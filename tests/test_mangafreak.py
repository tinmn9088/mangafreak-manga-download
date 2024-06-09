import mangafreak


def test_get_title_url_version():

    # arrange
    titles_expected_url_versions = {
        'FANTASY BISHOUJO JUNIKU OJISAN TO': 'fantasy_bishoujo_juniku_ojisan_to',
        'ISEKAI OJISAN': 'isekai_ojisan',
        'ISEKAI SHOKAN OJISAN NO JU MUSO LIFE SABAGE SUKI SALARY MAN HA KAISHA OWARI NI ISEKAI HE CHOKUKI SURU': 'isekai_shokan_ojisan_no_ju_muso_life_sabage_suki_salary_man_ha_kaisha_owari_ni_isekai_he_chokuki_suru',
        'TENSEI SHITE KARA 40-NEN. SOROSORO, OJI-SAN MO KOI GA SHITAI.': 'tensei_shite_kara_40_nen_sorosoro_oji_san_mo_koi_ga_shitai',
        'BORUTO: NARUTO NEXT GENERATIONS': 'boruto_naruto_next_generations',
        'MAIRIMASHITA! IRUMA-KUN': 'mairimashita_iruma_kun'
    }

    for title, expected_url_version in titles_expected_url_versions.items():

        # act
        actual = mangafreak.MangafreakService.get_title_url_version(title)

        # assert
        assert expected_url_version == actual


def test_add_leading_zeroes_digit_only_name():

    # arrange
    chapter_name = '43'
    length = 4
    expected = '0043'

    # act
    actual = mangafreak.MangafreakService.add_leading_zeroes(chapter_name, length)

    # assert
    assert expected == actual


def test_add_leading_zeroes_name_with_letters():

    # arrange
    chapter_name = '43e'
    length = 4
    expected = '0043e'

    # act
    actual = mangafreak.MangafreakService.add_leading_zeroes(chapter_name, length)

    # assert
    assert expected == actual
