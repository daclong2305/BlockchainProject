import json
import os

import pytest

from aave_analyst.llm import BedrockLLM


@pytest.fixture
def config_dir(tmp_path, monkeypatch):
    for name in list(os.environ):
        if name.startswith('AWS_') or name in {'BEDROCK_MODEL_ID', 'AAVE_PROJECT_ROOT'}:
            monkeypatch.delenv(name)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv('AWS_EC2_METADATA_DISABLED', 'true')
    monkeypatch.setenv('AWS_CONFIG_FILE', str(tmp_path / 'aws-config'))
    monkeypatch.setenv('AWS_SHARED_CREDENTIALS_FILE', str(tmp_path / 'aws-credentials'))
    return tmp_path


def test_env_keys_work_without_default_profile(config_dir):
    (config_dir / 'env').write_text(
        'AWS_ACCESS_KEY_ID=test-access\nAWS_SECRET_ACCESS_KEY=test-secret\n'
        'AWS_SESSION_TOKEN=\nAWS_DEFAULT_REGION=ap-southeast-1\n', encoding='utf-8')
    llm = BedrockLLM()
    assert llm.region == 'ap-southeast-1'
    session = llm.session()
    credentials = session.get_credentials().get_frozen_credentials()
    assert credentials.access_key == 'test-access'
    assert credentials.secret_key == 'test-secret'
    assert credentials.token is None
    assert 'test-secret' not in json.dumps(llm.config())


def test_process_environment_overrides_file_and_region_alias(config_dir, monkeypatch):
    (config_dir / 'env').write_text('AWS_REGION=us-east-1\nBEDROCK_MODEL_ID=file-model\n')
    monkeypatch.setenv('AWS_DEFAULT_REGION', 'eu-west-1')
    monkeypatch.setenv('BEDROCK_MODEL_ID', 'process-model')
    llm = BedrockLLM()
    assert llm.region == 'eu-west-1'
    assert llm.model_id == 'process-model'


def test_dotenv_quotes_comments_bom_and_temporary_token(config_dir):
    (config_dir / '.env').write_text(
        '# comment\nexport AWS_ACCESS_KEY_ID="test-access"\n'
        "AWS_SECRET_ACCESS_KEY='secret/with+=hash#' # comment\n"
        'AWS_SESSION_TOKEN=token/with+=\nAWS_DEFAULT_REGION=us-west-2 # comment\n',
        encoding='utf-8-sig')
    llm = BedrockLLM()
    credentials = llm.session().get_credentials().get_frozen_credentials()
    assert credentials.secret_key == 'secret/with+=hash#'
    assert credentials.token == 'token/with+='
    assert llm.region == 'us-west-2'


def test_env_takes_precedence_over_dotenv(config_dir):
    (config_dir / 'env').write_text('BEDROCK_MODEL_ID=env-model\n')
    (config_dir / '.env').write_text('BEDROCK_MODEL_ID=dotenv-model\n')
    assert BedrockLLM().model_id == 'env-model'


def test_profile_credentials_still_work(config_dir):
    (config_dir / 'env').write_text('AWS_PROFILE=research\n')
    (config_dir / 'aws-credentials').write_text(
        '[research]\naws_access_key_id=profile-access\naws_secret_access_key=profile-secret\n')
    credentials = BedrockLLM().session().get_credentials().get_frozen_credentials()
    assert credentials.access_key == 'profile-access'


def test_doctor_uses_same_credentials_without_exposing_secrets(config_dir, capsys):
    from aave_analyst.cli import doctor
    (config_dir / 'env').write_text('AWS_ACCESS_KEY_ID=test-access\nAWS_SECRET_ACCESS_KEY=test-secret\n')
    result = doctor()
    output = capsys.readouterr().out
    assert result['credentials_available'] is True
    assert 'test-access' not in output
    assert 'test-secret' not in output


def test_partial_keys_fail_without_leaking_values(config_dir):
    (config_dir / 'env').write_text('AWS_ACCESS_KEY_ID=private-access\n')
    with pytest.raises(ValueError) as error:
        BedrockLLM().session()
    assert 'private-access' not in str(error.value)


def test_invalid_line_error_does_not_echo_secret(config_dir):
    (config_dir / 'env').write_text('secret pasted without assignment\n')
    with pytest.raises(ValueError) as error:
        BedrockLLM()
    assert 'line 1' in str(error.value)
    assert 'secret pasted' not in str(error.value)
