import pytest

from code_two.postcodeuk import PostCodeUk


class TestPostCodeUk:

    valid_postcodes = [
        {'postcode': PostCodeUk('EC1A 1BB'), 'outward': 'EC1A', 'inward': '1BB'},
        {'postcode': PostCodeUk('W1A 0AX'), 'outward': 'W1A', 'inward': '0AX'},
        {'postcode': PostCodeUk('M1 1AE'), 'outward': 'M1', 'inward': '1AE'},
        {'postcode': PostCodeUk('B33 8TH'), 'outward': 'B33', 'inward': '8TH'},
        {'postcode': PostCodeUk('CR2 6XH'), 'outward': 'CR2', 'inward': '6XH'},
        {'postcode': PostCodeUk('DN55 1PT'), 'outward': 'DN55', 'inward': '1PT'},
    ]
    invalid_postcodes = [
        {'postcode': PostCodeUk('')},
        {'postcode': PostCodeUk('invalid')},
        {'postcode': PostCodeUk('CR2@ 6XH')},
        {'postcode': PostCodeUk('DN55-1PT')},
    ]

    @pytest.mark.parametrize('postcode', [
        None, 1, [],
    ])
    def test__init_invalid_postcode(self, postcode):
        with pytest.raises(TypeError):
            PostCodeUk(postcode)

    @pytest.mark.parametrize('valid_postcodes', valid_postcodes)
    def test_valid_postcode(self, valid_postcodes):
        assert valid_postcodes['postcode'].is_valid()

    @pytest.mark.parametrize('invalid_postcodes', invalid_postcodes)
    def test_in_valid_postcode(self, invalid_postcodes):
        assert not invalid_postcodes['postcode'].is_valid()

    @pytest.mark.parametrize('valid_postcodes', valid_postcodes)
    def test__valid_true(self, valid_postcodes):
        assert valid_postcodes['postcode']._valid()
        assert valid_postcodes['postcode'].get_outward() == valid_postcodes['outward']
        assert valid_postcodes['postcode'].get_inward() == valid_postcodes['inward']

    @pytest.mark.parametrize('invalid_postcodes', invalid_postcodes)
    def test__valid_false(self, invalid_postcodes):
        assert not invalid_postcodes['postcode']._valid()
        assert not invalid_postcodes['postcode'].get_outward()
        assert not invalid_postcodes['postcode'].get_inward()

    @pytest.mark.parametrize('postcode, expected_object', [
        ('EC1A 1BB', True), ('W1A 0AX', True), ('M1 1AE', True),
        ('', False), ('invalid', False)
    ])
    def test_validate(self, postcode, expected_object):
        if expected_object:
            assert PostCodeUk._validate(postcode)
        else:
            assert not PostCodeUk._validate(postcode)

    @pytest.mark.parametrize('valid_postcodes', valid_postcodes)
    def test_get_outward_valid(self, valid_postcodes):
        assert valid_postcodes['postcode'].get_outward() == valid_postcodes['outward']

    @pytest.mark.parametrize('invalid_postcodes', invalid_postcodes)
    def test_get_outward_valid(self, invalid_postcodes):
        assert not invalid_postcodes['postcode'].get_outward()

    @pytest.mark.parametrize('valid_postcodes', valid_postcodes)
    def test_get_inward_valid(self, valid_postcodes):
        assert valid_postcodes['postcode'].get_inward() == valid_postcodes['inward']

    @pytest.mark.parametrize('invalid_postcodes', invalid_postcodes)
    def test_get_inward_valid(self, invalid_postcodes):
        assert not invalid_postcodes['postcode'].get_inward()

    def test_random_postcode(self):
        for i in range(50):
            postcode = PostCodeUk(PostCodeUk.random_postcode())
            assert postcode.is_valid()

    @pytest.mark.parametrize('text, postcodes, expected', [
        ('Example of text with postcode W1A 0AX and other postcode'
         'EC1A 1BB', ['EC1A 1BB', 'W1A 0AX'], ['EC1A 1BB', 'W1A 0AX']),
        ('Other text with on postcode M1 1AE none postcodes informed', [], ['M1 1AE']),
        ('Other text withiout postcode', ['M1 1AE'], []),
    ])
    def test_find_all_in_text_valid(self, text, postcodes, expected):
        assert sorted(PostCodeUk.find_all_in_text(text, postcodes)) == sorted(expected)

    @pytest.mark.parametrize('text, postcodes, expected', [
        ('Example of text with postcode W1A 0AX and other postcode'
         'EC1A 1BB invalid post code informed', 1, TypeError),
        ('Other text with on postcode M1 1AE invalid postcodes informed', [10],
         'all postcodes should be valid'),
    ])
    def test_find_all_in_text_invalid(self, text, postcodes, expected):
        if expected == TypeError:
            with pytest.raises(TypeError):
                PostCodeUk.find_all_in_text(text, postcodes) == expected
        else:
            assert PostCodeUk.find_all_in_text(text, postcodes) == expected
