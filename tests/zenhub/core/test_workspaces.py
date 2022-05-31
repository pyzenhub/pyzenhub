from .data import REPO_ID, WORKSPACE_ID


def test_get_workspaces(zh):
    data = zh.get_workspaces(REPO_ID)
    assert data


def test_get_workspaces_model(zh):
    zh._output_models = True
    data = zh.get_workspaces(REPO_ID)
    assert data


def test_get_repository_board(zh):
    data = zh.get_repository_board(WORKSPACE_ID, REPO_ID)
    assert data


def test_get_oldest_repository_board(zh):
    data = zh.get_oldest_repository_board(REPO_ID)
    assert data
