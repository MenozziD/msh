from controller import Login


def test_no_username():
    data = ''
    assert Login.check(data)['output'] == 'Questa API ha bisogno di un payload'