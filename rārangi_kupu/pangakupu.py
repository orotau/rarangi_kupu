'''
The functions to get the data ready for the web site
'''

import maoriword as mw
import pataka
import pū
from collections import Counter
import pprint
import random

nines = (['āhikihiki',
 'āhiwahiwa',
 'āhuahanga',
 'āhuatanga',
 'āhukahuka',
 'āhumehume',
 'ahungarua',
 'ahupūngao',
 'āhuruhuru',
 'ahuwhenua',
 'ākahukahu',
 'akakopuka',
 'akapirita',
 'akawhenua',
 'ākirikiri',
 'amatiatia',
 'amiorangi',
 'ānewanewa',
 'āninanina',
 'āniwaniwa',
 'angotanga',
 'arearenga',
 'ariaringa',
 'āritarita',
 'aroarorua',
 'aroarotea',
 'ārohirohi',
 'aromahana',
 'ateatenga',
 'aupounamu',
 'āwakewake',
 'āwenewene',
 'awherangi',
 'āwhiowhio',
 'etokohinu',
 'eweewerau',
 'hakehakeā',
 'hangareka',
 'hangariki',
 'hangarite',
 'hangaruru',
 'hangatare',
 'hangatītī',
 'hāparangi',
 'harangote',
 'haukōpata',
 'haumaruru',
 'hautaonga',
 'hautaorua',
 'hauwhenua',
 'hikirangi',
 'hinapōuri',
 'hinengaro',
 'hīrairaka',
 'hīwaiwaka',
 'hokahokai',
 'hokehokeā',
 'hokowhitu',
 'honohonoā',
 'hōngongoi',
 'horahanga',
 'horomatua',
 'houkūmara',
 'houmāpara',
 'houmipara',
 'houtāwere',
 'huakaroro',
 'huawhenua',
 'huihuinga',
 'hukāpunga',
 'hukāwhatu',
 'hūngongoi',
 'hurikōtua',
 'hurumaeko',
 'hutupaoro',
 'hututawai',
 'inakuanei',
 'inatahirā',
 'iringatau',
 'iwituaroa',
 'kaharunga',
 'kahikatea',
 'kahikātoa',
 'kahurangi',
 'kaiāwhina',
 'kaihaukai',
 'kaihōtaka',
 'kaikairau',
 'kaikaitio',
 'kaikanohi',
 'kaikawaka',
 'kaikōhure',
 'kaikōmako',
 'kaikōpura',
 'kaikōraka',
 'kaikōrero',
 'kaimomotu',
 'kaingākau',
 'kaingarua',
 'kaioraora',
 'kaipākehā',
 'kaipakihi',
 'kaipākūhā',
 'kaiparore',
 'kairāwaru',
 'kairēhita',
 'kaitorohi',
 'kaiwaenga',
 'kaiwhiria',
 'kakapohai',
 'kakapowai',
 'kākaramea',
 'kākarangū',
 'kākarauri',
 'kakarewao',
 'kakaruwai',
 'kakerangi',
 'kanaekura',
 'kaniawhea',
 'kanokanoā',
 'kaparangi',
 'kapuranga',
 'kapurangi',
 'karakahia',
 'karangatā',
 'karapetau',
 'karariwha',
 'karatiwha',
 'karawheta',
 'karawhiti',
 'karehākoa',
 'kārikiuri',
 'karupango',
 'kātuarehe',
 'kauaeraro',
 'kauanuanu',
 'kauhauora',
 'kauhoehoe',
 'kauhouora',
 'kauhuahua',
 'kaumahaki',
 'kaunihera',
 'kauopeope',
 'kaupāpari',
 'kaupāparu',
 'kaupararī',
 'kaurerehu',
 'kautārere',
 'kauwaemua',
 'kauwhanga',
 'kawaupaka',
 'kawekaweā',
 'kēkerengū',
 'kēkerewai',
 'keokeonga',
 'kerehunga',
 'keretewha',
 'kikiwhara',
 'kikorangi',
 'kikowhiti',
 'kirimangu',
 'kiripuaki',
 'kiriwhero',
 'kiwitaiki',
 'kōhoimako',
 'kōhoperoa',
 'kohurangi',
 'koitareke',
 'kōkōrangi',
 'kōkorouri',
 'kokotaiko',
 'kokotiate',
 'kokotiuru',
 'kōkōtonga',
 'kōmakohua',
 'konganuku',
 'kōpūpūtai',
 'korirangi',
 'koroātito',
 'korohunga',
 'koromatua',
 'korongatā',
 'koropetau',
 'kororangi',
 'kororiwha',
 'korotaiko',
 'korotiwha',
 'korotuohu',
 'koroukore',
 'korowhiti',
 'korutanga',
 'koukouoro',
 'kōurapaka',
 'kourepoua',
 'koutareke',
 'kuikuinga',
 'kūkāwhare',
 'kūkukuroa',
 'kūkūpango',
 'kūkuruatu',
 'kūmarahou',
 'kurahaupō',
 'kuruwhetu',
 'mahurangi',
 'makahinga',
 'makaweroa',
 'makawhiti',
 'makitaunu',
 'mākuratea',
 'manapōuri',
 'manatārua',
 'manatunga',
 'manawanui',
 'manemanea',
 'maninohea',
 'mānukaroa',
 'manumanuā',
 'manuwhiri',
 'mangainga',
 'mangamutu',
 'mangōpare',
 'māpauriki',
 'māpouriki',
 'marakihau',
 'marariwha',
 'māreikura',
 'maruatata',
 'marurenga',
 'mataauahi',
 'matahīapo',
 'matakapua',
 'matakiore',
 'matakīrea',
 'matakūrae',
 'mātangata',
 'mātāngohi',
 'matapōuri',
 'matatengi',
 'matatewha',
 'matawhaia',
 'matawhero',
 'maumahara',
 'maungarua',
 'meatingia',
 'meingatia',
 'mihingare',
 'mokamokai',
 'mokepūihi',
 'mokotawhā',
 'mokowhiti',
 'mōmōhanga',
 'momotawai',
 'motopaika',
 'motuhanga',
 'motuhenga',
 'motuoruhi',
 'motupaika',
 'murikōkai',
 'murukōkai',
 'namunamuā',
 'naoakenui',
 'nawakenui',
 'nōnāianei',
 'nonorangi',
 'nukaparau',
 'ngāekieki',
 'ngāeroero',
 'ngāhoahoa',
 'ngākaunui',
 'ngākaurua',
 'ngākoikoi',
 'ngāoheohe',
 'ngāoraora',
 'ngāoriori',
 'ngaropoko',
 'ngāruerue',
 'ngatahure',
 'ngātatahi',
 'ngātātata',
 'ngawhewhe',
 'ngongirua',
 'ngongohau',
 'ngongotua',
 'ngoungoua',
 'ngōuruuru',
 'ngutukura',
 'ngututahi',
 'oeamarama',
 'oneharuru',
 'onekōkopu',
 'ōpurepure',
 'ōramarama',
 'ōrangitea',
 'pahoreroa',
 'paiahaaha',
 'paihikara',
 'paioneone',
 'pākaurere',
 'pākihiroa',
 'pakiranga',
 'pakiwhara',
 'pangakupu',
 'pāpāhenga',
 'papahuaki',
 'papaihore',
 'papakairā',
 'papakiuma',
 'pāpakiuma',
 'papangoko',
 'paparahua',
 'paparanga',
 'pāpāringa',
 'pāpātanga',
 'papawheki',
 'parahaere',
 'parahanga',
 'paraikete',
 'parakaeto',
 'parakiwai',
 'parakuihi',
 'parangunu',
 'paraparau',
 'parataiao',
 'paratūtae',
 'pareārohi',
 'parengaru',
 'parewhero',
 'parumoana',
 'pārurenga',
 'patapatai',
 'pātikinui',
 'patungaro',
 'pēhiakura',
 'pekerangi',
 'pēperekōu',
 'perehunga',
 'pīkaraihe',
 'pikiarero',
 'pipiauroa',
 'pipiharau',
 'pīrairaka',
 'pirapirau',
 'pirihonga',
 'pirihonge',
 'pirihongo',
 'pīwaiwaka',
 'poikōpiko',
 'poitūkohu',
 'pōkaikaha',
 'pokerenoa',
 'pokokohua',
 'pokokōhua',
 'pōkokohua',
 'pokotiwha',
 'pongakawa',
 'popokanua',
 'pōpokorua',
 'pōpokotea',
 'pōrauraha',
 'poreirewa',
 'poroāwhio',
 'porohanga',
 'porongāua',
 'porongāue',
 'pororangi',
 'pōrorotua',
 'porowhita',
 'pōtaitaka',
 'pouhihiri',
 'poupoutea',
 'pourērere',
 'poutahaki',
 'poutāpeta',
 'poutārewa',
 'poutūmārō',
 'pouwhenua',
 'pouwhiwhi',
 'pūāhaehae',
 'puatataua',
 'puhawaiki',
 'puipuiaki',
 'pūkekotia',
 'pūkororoa',
 'pukuaroha',
 'pukumaire',
 'pukutenga',
 'pungarehu',
 'pungatara',
 'pūohotata',
 'pūrahorua',
 'puramorua',
 'purawhetū',
 'pūrereahu',
 'pūrerehua',
 'purumorua',
 'pūtaihinu',
 'pūtakenga',
 'pūtaringa',
 'pūtauhinu',
 'rāinaoake',
 'rāitahirā',
 'rāitarihā',
 'rangamaro',
 'rangatahi',
 'rangataua',
 'rangatira',
 'ranginamu',
 'rangiriri',
 'rangiroro',
 'rangitahi',
 'rangitaro',
 'rangitihi',
 'rangitoto',
 'rangiwaho',
 'raumahara',
 'raumahehe',
 'raumarire',
 'raumaroke',
 'raungaiti',
 'rauparaha',
 'rautākiri',
 'rawahanga',
 'rengapapā',
 'rimurehia',
 'ringakore',
 'ringatahi',
 'ringawera',
 'riroriroi',
 'rongokere',
 'rongoteka',
 'rongowaha',
 'rōtaringa',
 'ruatapuke',
 'rūrūtaina',
 'taetaeata',
 'tahamoana',
 'taharangi',
 'tahatonga',
 'tahumaero',
 'tahurangi',
 'taiahoaho',
 'taihoropī',
 'tāikarehā',
 'taikoraha',
 'tāinanahi',
 'tāinaoake',
 'tāingāwai',
 'taiohinga',
 'taioreore',
 'taiororua',
 'taipakeke',
 'taitāhake',
 'taitakoto',
 'tāitarihā',
 'taiwhanga',
 'taiwhenua',
 'takaānini',
 'takaāwhio',
 'takahanga',
 'tākaikaha',
 'takarangi',
 'takatakai',
 'takatāpui',
 'takawhaki',
 'takawheta',
 'takawhita',
 'takawhiti',
 'tākekenga',
 'tākirikau',
 'takurangi',
 'tamararea',
 'tāngangao',
 'tangariki',
 'tangimeme',
 'tangiweto',
 'tāpākūwhā',
 'taparenga',
 'tapurangi',
 'tarahanga',
 'tarakakao',
 'tarāpunga',
 'taratarai',
 'tarawhata',
 'tarawhatu',
 'tarawhete',
 'tarawhiti',
 'tārukenga',
 'tātāhoata',
 'tātaihore',
 'tataramoa',
 'tātarāmoa',
 'tātaruwai',
 'tauhounga',
 'taukahiwi',
 'taukahore',
 'taukaikai',
 'taumarere',
 'taumārere',
 'taumataua',
 'taunanawe',
 'tauonioni',
 'taupaepae',
 'tauparoro',
 'taupatiti',
 'taupokina',
 'taupupuni',
 'taurereka',
 'taurikura',
 'tautauhea',
 'tautaunga',
 'tautētete',
 'tautotohe',
 'tauutuutu',
 'tauwhanga',
 'tauwhiwhi',
 'tāwharara',
 'tāwhewheo',
 'tētēaweka',
 'tetērongo',
 'tiakākahi',
 'tihotihoi',
 'tinetinei',
 'tinihanga',
 'tīparenui',
 'tīrairaka',
 'tīraumoko',
 'tīraureka',
 'tīrauweke',
 'tiriwhana',
 'tirohanga',
 'tīwaiwaka',
 'tiwhikete',
 'tohemanga',
 'tokamatua',
 'tokerangi',
 'tokomanga',
 'tokomatua',
 'tokomauri',
 'tokopuaha',
 'tokorangi',
 'tomokanga',
 'tōngāmimi',
 'tongarewa',
 'tōrangapū',
 'torohanga',
 'torowhiti',
 'totokepio',
 'totokipia',
 'totokipio',
 'totoriwai',
 'tōtoroene',
 'tōuarangi',
 'toutouwai',
 'tuakahiwi',
 'tuakaihau',
 'tuaukiuki',
 'tuauriuri',
 'tuawahine',
 'tuawhenua',
 'tūhauwiri',
 'tūhawaiki',
 'tūkirunga',
 'tukupunga',
 'tukurangi',
 'tūmataiti',
 'tūmatanui',
 'tūmatarau',
 'tūngāwiri',
 'tūparehua',
 'tupurangi',
 'tūreikura',
 'turiwhati',
 'turiwhatu',
 'turuhunga',
 'turuturua',
 'turuwhatu',
 'tūtaeatua',
 'tūtaemanu',
 'tuturuatu',
 'tūwaharoa',
 'uauawhiti',
 'upokororo',
 'upokotaua',
 'urukōwhao',
 'uruwhenua',
 'waenganui',
 'wahangohi',
 'waiārangi',
 'waihīrere',
 'waikākahi',
 'waikauere',
 'waingōhia',
 'wairuatoa',
 'wairurutu',
 'waitākiri',
 'wakapīhau',
 'warehenga',
 'wikitōria',
 'whāereere',
 'whaihanga',
 'whāitaita',
 'whaiwhaiā',
 'whakaahua',
 'whakaanea',
 'whakaanga',
 'whakaangi',
 'whakaatea',
 'whakaauau',
 'whakaawhi',
 'whakaeaea',
 'whakahāhā',
 'whakahana',
 'whakahara',
 'whakahawe',
 'whakaheke',
 'whakahemo',
 'whakahere',
 'whakahewa',
 'whakahīhī',
 'whakahina',
 'whakahīoi',
 'whakahipa',
 'whakahiwa',
 'whakahōhā',
 'whakahoho',
 'whakahoki',
 'whakahope',
 'whakahopo',
 'whakahore',
 'whakahori',
 'whakahoro',
 'whakaioio',
 'whakakahu',
 'whakakaka',
 'whakakapi',
 'whakakāti',
 'whakakeke',
 'whakakewa',
 'whakakikī',
 'whakakīkī',
 'whakakiko',
 'whakakini',
 'whakakino',
 'whakakitā',
 'whakakite',
 'whakakoha',
 'whakakoia',
 'whakakoki',
 'whakakoko',
 'whakakopa',
 'whakakōpē',
 'whakakopi',
 'whakakore',
 'whakakoro',
 'whakakukū',
 'whakakumu',
 'whakakuru',
 'whakamahi',
 'whakamahu',
 'whakamāhu',
 'whakamama',
 'whakamana',
 'whakamanu',
 'whakamara',
 'whakamārō',
 'whakamātā',
 'whakamate',
 'whakamene',
 'whakamiha',
 'whakamihi',
 'whakamine',
 'whakamira',
 'whakamito',
 'whakamoho',
 'whakamōkā',
 'whakamoke',
 'whakamono',
 'whakamōtī',
 'whakamōtu',
 'whakanako',
 'whakanānā',
 'whakanano',
 'whakananu',
 'whakanene',
 'whakanewa',
 'whakaniko',
 'whakanoho',
 'whakanuka',
 'whakanumi',
 'whakangao',
 'whakangau',
 'whakaoioi',
 'whakapāha',
 'whakapāho',
 'whakapaki',
 'whakapako',
 'whakapapa',
 'whakapāpā',
 'whakaparo',
 'whakaparu',
 'whakapata',
 'whakapati',
 'whakapeau',
 'whakapēhi',
 'whakapeka',
 'whakapeke',
 'whakapeti',
 'whakapiki',
 'whakapiko',
 'whakapipi',
 'whakapiri',
 'whakapohe',
 'whakapono',
 'whakapopo',
 'whakapopō',
 'whakaporo',
 'whakapuhi',
 'whakapuke',
 'whakapuku',
 'whakapupū',
 'whakapuru',
 'whakaputa',
 'whakaputu',
 'whakarahi',
 'whakaraka',
 'whakarake',
 'whakaranu',
 'whakarapa',
 'whakarara',
 'whakarare',
 'whakararu',
 'whakarato',
 'whakarehu',
 'whakareka',
 'whakarera',
 'whakarere',
 'whakarētō',
 'whakarewa',
 'whakarika',
 'whakariri',
 'whakariro',
 'whakarite',
 'whakaroau',
 'whakarōpū',
 'whakaruke',
 'whakaruku',
 'whakaruru',
 'whakarūrū',
 'whakatahe',
 'whakataka',
 'whakatakē',
 'whakataki',
 'whakatara',
 'whakatare',
 'whakatari',
 'whakatata',
 'whakatehe',
 'whakateka',
 'whakateke',
 'whakatene',
 'whakatepe',
 'whakatere',
 'whakatete',
 'whakatihi',
 'whakatika',
 'whakatiki',
 'whakatina',
 'whakatipi',
 'whakatipu',
 'whakatito',
 'whakatohe',
 'whakatoke',
 'whakatomo',
 'whakatonu',
 'whakatopa',
 'whakatoro',
 'whakatuma',
 'whakatupu',
 'whakaturi',
 'whakatutu',
 'whakauaua',
 'whakauwhi',
 'whakawaha',
 'whakawahi',
 'whakaware',
 'whakawehe',
 'whakaweto',
 'whakawiri',
 'whakawhiu',
 'whākoekoe',
 'whānāriki',
 'whanaunga',
 'whāngongo',
 'whāomoomo',
 'whārarahi',
 'wharariki',
 'wharaunga',
 'wharauroa',
 'wharehinu',
 'wharekano',
 'wharekura',
 'wharepaku',
 'wharepuni',
 'wharerohi',
 'whāruarua',
 'whātaitai',
 'whatīanga',
 'whātītipa',
 'whatitiri',
 'whatitoka',
 'whatukihi',
 'whatukuhu',
 'whatukura',
 'whatutoto',
 'whātuturi',
 'whāuraura',
 'whāwhākou',
 'whāwhārua',
 'wheawheau',
 'wheketere',
 'whēorooro',
 'whetūriki',
 'whewhengi',
 'whiorangi',
 'whirinaki',
 'whitianga',
 'whitihoro',
 'whiwhinga',
 'whīwhiwhi',
 'whutupōro'])


def get_all_koru(seed_word):
    ''' 
    Takes a 9 letter Māori seed_word, e.g. pangakupu
    and returns one representative koru from each ponga
    At this stage there is no guarantee that the digraphs
    are in what I would call 'ok' positions
    Also no guarantee that the seed_word is disguised.
    '''
    seed_word_as_list = mw._aslist(seed_word)
    seed_word_letters = [x for x in seed_word_as_list if len(x) == 1] #no digraphs
    
    for letter in set(seed_word_letters):
        #move the letter to the end of the word
        koru = seed_word_as_list
        koru.append(koru.pop(koru.index(letter))) #move the letter to the end
        koru = ''.join(koru)
        koru_children = pataka.get_children(koru)
        print (seed_word)
        print (koru[-1])
        print (koru_children)
        print (len(koru_children))

def get_nines_structure():
    nines_as_list = [mw._aslist(x) for x in nines]
    nines_structure = []
    for nine_as_list in nines_as_list:
        nine_as_list = ['V' if x in pū.vowels + pū.macronised_vowels else x for x in nine_as_list]
        nine_as_list = ['D' if len(x) == 2 else x for x in nine_as_list]
        nine_as_list = ['C' if x in pū.consonants else x for x in nine_as_list]
        nines_structure.append(nine_as_list)
    
    counts = []
    for nine_structure in nines_structure:
        ns_count = Counter(nine_structure)
        ns_count = dict(ns_count)
        ns_count = list(ns_count.items())
        counts.append(tuple(ns_count))
    
    d =  Counter(counts)
    pprint.pprint(d)


def get_seed_word_structure(seed_word=None):

    if seed_word is None:
        seed_word = random.choice(nines)
        
    seed_word_as_list = mw._aslist(seed_word)
    seed_word_structure = seed_word_as_list
    seed_word_structure = ['V' if x in pū.vowels + pū.macronised_vowels else x for x in seed_word_structure]
    seed_word_structure = ['D' if len(x) == 2 else x for x in seed_word_structure]
    seed_word_structure = ['C' if x in pū.consonants else x for x in seed_word_structure]
   
    print (seed_word, dict(Counter(seed_word_structure)))
    return dict(Counter(seed_word_structure))


def get_koru(seed_word=None):

    if seed_word is None:
        seed_word = random.choice(nines)

    seed_word_structure = get_seed_word_structure(seed_word) #why?

    koru = [None] * 9 #initialise koru

    #listify the seed word and split into single letters and digraphs
    seed_word_as_list = mw._aslist(seed_word)
    single_letters = [x for x in seed_word_as_list if x in pū.all_single_letters] #will be emptied
    digraphs = [x for x in seed_word_as_list if x in pū.digraphs] #will be emptied

    #randomly select 'centre letter' and remove it from single letters
    centre_letter = random.choice(single_letters)
    single_letters.remove(centre_letter)

    #add 'centre letter' to koru, 8 squares remaining to be filled
    koru[8] = centre_letter


    #randomly select and randomly place the digraphs (if any)
    #note there are constraints to the randomness
    if digraphs:
        #establish the squares where it is ok to put digraphs
        if centre_letter in pū.duals_left: #w or n
            #avoid 'vertical digraphs'
            ok_digraph_squares = [(1,2),(5,4)]
        elif centre_letter in pū.duals_right: #h
            #avoid 'vertical digraphs'
            ok_digraph_squares = [(0,1),(6,5)]
        else:
            #'vertical digraphs' not an issue
            ok_digraph_squares = [(0,1),(1,2),(5,4),(6,5)]

        digraphs_count = len(digraphs)

        if digraphs_count == 1 or digraphs_count == 2:
            #randomly select 'digraph1' and remove it from digraphs
            digraph1 = random.choice(digraphs)
            digraphs.remove(digraph1)

            #randomly select the squares for 'digraph1'
            digraph1_square = random.choice(ok_digraph_squares)

            #add 'digraph1' to koru
            koru[digraph1_square[0]] = digraph1[0] #7 squares remaining
            koru[digraph1_square[1]] = digraph1[1] #6 squares remaining

            if digraphs_count == 2:
                #select 'digraph2' and remove it from digraphs
                digraph2 = random.choice(digraphs)
                digraphs.remove(digraph2)

                #place the 2nd digraph directly above or below the first
                if digraph1_square == (0,1) : digraph2_square = (6,5)
                if digraph1_square == (6,5) : digraph2_square = (0,1)
                if digraph1_square == (1,2) : digraph2_square = (5,4)
                if digraph1_square == (5,4) : digraph2_square = (1,2)

                #add 'digraph2 to koru'
                koru[digraph2_square[0]] = digraph2[0] #5 squares remaining
                koru[digraph2_square[1]] = digraph2[1] #4 squares remaining


    #place the rest of the single letters
    if digraphs_count == 2:
            #4 squares remaining
            #we may have 1 consonant to place in a specific position
            remaining_consonant = [x for x in single_letters if x in pū.consonants]
            if remaining_consonant:
                if digraph1_square == (0,1) or digraph1_square == (6,5):
                    koru[3] = remaining_consonant[0]
                else:
                    koru[7] = remaining_consonant[0]
                single_letters.remove(remaining_consonant[0])
            
            #randomly assign the remaining single letters (should all be vowels)
            #3 or 4 remaining
            for index, square in enumerate(koru):
                if square is None:
                    letter_to_place = random.choice(single_letters)
                    single_letters.remove(letter_to_place)
                    koru[index] = letter_to_place

            #DONE for 2 digraphs

    if digraphs_count == 1 and centre_letter in pū.consonants:
        #6 letters remaining to place, of which at least 4 will be vowels

    print(koru)
                    
            
        

    

    

    

    


if __name__ == '__main__':

    import sys
    import argparse
    import pprint
    import ast


    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the get_all_koru function
    get_all_koru_parser = subparsers.add_parser('get_all_koru')
    get_all_koru_parser.add_argument('seed_word')
    get_all_koru_parser.set_defaults(function = get_all_koru)

    # create the parser for the get_nines_structure function
    get_nines_structure_parser = subparsers.add_parser('get_nines_structure')
    get_nines_structure_parser.set_defaults(function = get_nines_structure)

    # create the parser for the get_seed_word_structure function
    get_seed_word_structure_parser = subparsers.add_parser('get_seed_word_structure')
    get_seed_word_structure_parser.add_argument('-seed_word')
    get_seed_word_structure_parser.set_defaults(function = get_seed_word_structure)

    # create the parser for the get_koru function
    get_koru_parser = subparsers.add_parser('get_koru')
    get_koru_parser.add_argument('-seed_word')
    get_koru_parser.set_defaults(function = get_koru)

    # parse the arguments
    arguments = parser.parse_args()
    arguments = vars(arguments) #convert from Namespace to dict

    #attempt to extract and then remove the function entry
    try:
        function_to_call = arguments['function'] 
    except KeyError:
        #python pangakupu.py entered on command line (a function name is required)
        print ("You need a function name. Please type -h to get help")
        sys.exit()
    else:
        #remove the function entry
        del arguments['function']
    
    if arguments:
        #remove any entries that have a value of 'None'
        #We are *assuming* that these are optional
        #We are doing this because we want the function definition to define
        #the defaults (NOT the function call)
        arguments = { k : v for k,v in arguments.items() if v is not None }

        #alter any string 'True' or 'False' to bools
        arguments = { k : ast.literal_eval(v) if v in ['True','False'] else v 
                                              for k,v in arguments.items() }       

    result = function_to_call(**arguments) #note **arguments works fine for empty dict {}
