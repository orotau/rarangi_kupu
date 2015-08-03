def test_list_sorting():
    from random import shuffle

    #Test ONLY ascending sorts

    #at the most basic level macronised vowels are treated as unmacronised
    basic_group = ['aroha', 'ēhea', 'hauiti'] #the correct ascending order
    shuffle(basic_group)
    basic_group_shuffled = basic_group
    assert sorted(basic_group_shuffled, key=mw._get_list_sort_key) == ['aroha', 'ēhea', 'hauiti']
    assert sorted(basic_group_shuffled, key=mw._get_list_sort_key) != sorted(basic_group_shuffled)

    #the sort will disregard any dash(es)
    dash_group = ['takini', 'Taki-o-Autahi', 'Takirā'] #the correct ascending order
    shuffle(dash_group)
    dash_group_shuffled = dash_group
    assert sorted(dash_group_shuffled, key=mw._get_list_sort_key) == ['takini', 'Taki-o-Autahi', 'Takirā']
    #dash sorts before letters asciibetically
    assert sorted(dash_group_shuffled, key=mw._get_list_sort_key) != sorted(dash_group_shuffled)

    #the sort will disregard any space(s)
    space_group = ['tuturuatu', 'tuturu pourewa', 'tuturuwhatu'] #the correct ascending order
    shuffle(space_group)
    space_group_shuffled = space_group
    assert sorted(space_group_shuffled, key=mw._get_list_sort_key) == ['tuturuatu', 'tuturu pourewa', 'tuturuwhatu']
    #space sorts before letters asciibetically
    assert sorted(space_group_shuffled, key=mw._get_list_sort_key) != sorted(space_group_shuffled)

    #order when words differ only by macron
    kaka4 = ['kaka', 'kakā', 'kāka', 'kākā'] #the correct ascending order
    shuffle(kaka4)
    kaka4_shuffled = kaka4
    assert sorted(kaka4_shuffled, key=mw._get_list_sort_key) == ['kaka', 'kakā', 'kāka', 'kākā']

    #order for digraph 'ng'
    digraph_ng_3 = ['tunehe', 'tunu', 'tunga'] #the correct ascending order
    shuffle(digraph_ng_3)
    digraph_ng_3_shuffled = digraph_ng_3
    assert sorted(digraph_ng_3_shuffled, key=mw._get_list_sort_key) == ['tunehe', 'tunu', 'tunga']
    assert sorted(digraph_ng_3_shuffled, key=mw._get_list_sort_key) != sorted(digraph_ng_3_shuffled)

    #order for digraph 'wh'
    digraph_wh_3 = ['kawe', 'kawiti', 'kawhe'] #the correct ascending order
    shuffle(digraph_wh_3)
    digraph_wh_3_shuffled = digraph_wh_3
    assert sorted(digraph_wh_3_shuffled, key=mw._get_list_sort_key) == ['kawe', 'kawiti', 'kawhe']
    assert sorted(digraph_wh_3_shuffled, key=mw._get_list_sort_key) != sorted(digraph_wh_3_shuffled)

    #order when words differ only by case
    assert sorted(['kahurangi','Kahurangi'], key=mw._get_list_sort_key) == ['Kahurangi', 'kahurangi']
    assert sorted(['Kahurangi','kahurangi'], key=mw._get_list_sort_key) == ['Kahurangi', 'kahurangi']

    #the one identifiable difference with HPK
    assert sorted(['Tāne', 'tane', 'tāne'], key=mw._get_list_sort_key) == ['tane', 'Tāne', 'tāne']
