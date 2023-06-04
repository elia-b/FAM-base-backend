import copier
import pytest
import pathlib
import prompt_toolkit.validation

@pytest.fixture(scope="session")
def copier_config_path() -> pathlib.Path:
    return pathlib.Path(__file__).parent.parent

@pytest.fixture
def test_data() -> dict:
    return {
        "author_name": "Test Name",
        "author_email": "test@email.test",
        "project_name": "ProjectName",
        "module_name": "test_api",
        "project_license": "MIT License"
    }

def test_template_generation(tmpdir, copier_config_path, test_data):
    copier.run_copy(copier_config_path.as_posix(), tmpdir, data=test_data)
    assert [
        basedir.name for basedir in pathlib.Path(tmpdir).glob('*')
        ] == [test_data["project_name"]]
    
    assert [
        file.name for file in pathlib.Path(tmpdir).glob('**/*') if file.is_file()
        ] == [
        'LICENSE', 
        '.copier-answers.yml', 
        'README.md'
        ]



@pytest.mark.parametrize(
        "author_name",
        [
            "?",
            "2test"
        ]
)
def test_validator_author_name(tmpdir, copier_config_path, test_data, author_name):
    expected = ("The author name must start with a letter, "
                "followed by one or more letters, digits, "
                "spaces or dashes all lowercase.")
    test_data["author_name"] = author_name
    with pytest.raises(prompt_toolkit.validation.ValidationError) as e:
        copier.run_copy(copier_config_path.as_posix(), tmpdir, data=test_data)
    assert e.value.message == expected


@pytest.mark.parametrize(
        "author_email",
        [
            "test",
            "test@2",
            "test@three."
        ]
)
def test_validator_author_email(tmpdir, copier_config_path, test_data, author_email):
    expected = ("The e-mail seems to be not valid, try again. "
                "If this message persist contact the maintainers of this repo.")
    test_data["author_email"] = author_email
    with pytest.raises(prompt_toolkit.validation.ValidationError) as e:
        copier.run_copy(copier_config_path.as_posix(), tmpdir, data=test_data)
    assert e.value.message == expected

@pytest.mark.parametrize(
        "project_name",
        [
             "?",
            "2test"
        ]
)
def test_validator_project_name(tmpdir, copier_config_path, test_data, project_name):
    expected = ("The project name must start with a letter, "
                "followed by one or more letters, digits or underscore or dash.")
    test_data["project_name"] = project_name
    with pytest.raises(prompt_toolkit.validation.ValidationError) as e:
        copier.run_copy(copier_config_path.as_posix(), tmpdir, data=test_data)
    assert e.value.message == expected

@pytest.mark.parametrize(
        "module_name",
        [
             "?",
            "2test"
            "A"
        ]
)
def test_validator_module_name(tmpdir, copier_config_path, test_data, module_name):
    expected = ("The module name must start with a letter, "
                "followed by one or more letters, digits "
                "or underscore all lowercase.")
    test_data["module_name"] = module_name
    with pytest.raises(prompt_toolkit.validation.ValidationError) as e:
        copier.run_copy(copier_config_path.as_posix(), tmpdir, data=test_data)
    assert e.value.message == expected


@pytest.mark.parametrize(
        "project_license",
        [
            "GPL2",
        ]
)
def test_validator_project_license(tmpdir, copier_config_path, test_data, project_license):
    expected = "Invalid choice"
    test_data["project_license"] = project_license
    with pytest.raises(ValueError) as e:
        copier.run_copy(copier_config_path.as_posix(), tmpdir, data=test_data)
    assert str(e.value) == expected