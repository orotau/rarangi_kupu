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

def get_seed_word_structure(seed_word=None):

    if seed_word is None:
        seed_word = random.choice(nines)
        
    seed_word_as_list = mw._aslist(seed_word)
    seed_word_structure = seed_word_as_list
    seed_word_structure = ['V' if x in pū.vowels + pū.macronised_vowels else x for x in seed_word_structure]
    seed_word_structure = ['D' if len(x) == 2 else x for x in seed_word_structure]
    seed_word_structure = ['C' if x in pū.consonants else x for x in seed_word_structure]
   
    #print (seed_word, dict(Counter(seed_word_structure)))
    return dict(Counter(seed_word_structure))


def get_nines_subset():

    consts = []
    for nine in nines:
        nine_structure = get_seed_word_structure(nine)
        if nine_structure['V'] == 4 and nine_structure['D'] == 1 and nine_structure['C'] == 3:
            nine_consts = [x for x in mw._aslist(nine) if x in pū.consonants]
            if 'w' in nine_consts:
                print (nine, nine_consts)
            consts.append(nine_consts)
    
    #c = Counter(tuple(consts))
    #print(c)
    #pprint.pprint(consts)
    return
                  


def get_koru(seed_word=None):

    if seed_word is None:
        seed_word = random.choice(nines)

    koru = [None] * 9 #initialise koru

    #listify the seed word and split into single letters and digraphs
    seed_word_as_list = mw._aslist(seed_word)
    single_letters = [x for x in seed_word_as_list if x in pū.all_single_letters] #will be emptied
    digraphs = [x for x in seed_word_as_list if x in pū.digraphs] #will be emptied
    digraphs_count = len(digraphs)

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

        if digraphs_count == 1 or digraphs_count == 2:
            #randomly select 'digraph1' and remove it from digraphs
            digraph1 = random.choice(digraphs)
            digraphs.remove(digraph1)

            #randomly select the squares for 'digraph1'
            digraph1_squares = random.choice(ok_digraph_squares)

            #add 'digraph1' to koru
            koru[digraph1_squares[0]] = digraph1[0] #7 squares remaining
            koru[digraph1_squares[1]] = digraph1[1] #6 squares remaining

            if digraphs_count == 2:
                #select 'digraph2' and remove it from digraphs
                digraph2 = random.choice(digraphs) #should only be 1 left
                digraphs.remove(digraph2)

                #place the 2nd digraph directly above or below the first
                if digraph1_squares == (0,1) : digraph2_squares = (6,5)
                if digraph1_squares == (6,5) : digraph2_squares = (0,1)
                if digraph1_squares == (1,2) : digraph2_squares = (5,4)
                if digraph1_squares == (5,4) : digraph2_squares = (1,2)

                #add 'digraph2 to koru'
                koru[digraph2_squares[0]] = digraph2[0] #5 squares remaining
                koru[digraph2_squares[1]] = digraph2[1] #4 squares remaining
    #End of Placing Digraphs


    #place the rest of the single letters (aside from that in the centre)
    if digraphs_count == 2:
            #4 squares remaining
            #we may have 1 consonant to place in a specific position
            remaining_consonant = [x for x in single_letters if x in pū.consonants]
            if remaining_consonant:
                if digraph1_squares == (0,1) or digraph1_squares == (6,5):
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

    if digraphs_count == 1:
        #6 letters remaining to place, of which at least 4 will be vowels

        #get *empty square on digraph row*
        if digraph1_squares == (0,1) : empty_square_on_digraph_row = 2
        if digraph1_squares == (1,2) : empty_square_on_digraph_row = 0
        if digraph1_squares == (6,5) : empty_square_on_digraph_row = 4
        if digraph1_squares == (5,4) : empty_square_on_digraph_row = 6

        #the *empty square on the digraph row* must have a vowel in it
        letter_to_place = random.choice([x for x in single_letters if x in pū.all_vowels])
        single_letters.remove(letter_to_place)
        koru[empty_square_on_digraph_row] = letter_to_place #5 squares remaining

        #get *empty square underneath or above the digraph*
        if digraph1_squares == (0,1) : empty_square_underneath_or_above_the_digraph = 7
        if digraph1_squares == (1,2) : empty_square_underneath_or_above_the_digraph = 3
        if digraph1_squares == (6,5) : empty_square_underneath_or_above_the_digraph = 7
        if digraph1_squares == (5,4) : empty_square_underneath_or_above_the_digraph = 3

        #the *empty square underneath or above the digraph* must have a vowel in it
        letter_to_place = random.choice([x for x in single_letters if x in pū.all_vowels])
        single_letters.remove(letter_to_place)
        koru[empty_square_underneath_or_above_the_digraph] = letter_to_place #4 squares remaining

        #get the *empty square in the middle column*
        if digraph1_squares == (0,1) : empty_square_middle_column = 5
        if digraph1_squares == (1,2) : empty_square_middle_column = 5
        if digraph1_squares == (6,5) : empty_square_middle_column = 1
        if digraph1_squares == (5,4) : empty_square_middle_column = 1

        #the *empty square in the middle column* must have a vowel in it
        letter_to_place = random.choice([x for x in single_letters if x in pū.all_vowels])
        single_letters.remove(letter_to_place)
        koru[empty_square_middle_column] = letter_to_place #3 squares remaining


    if digraphs_count == 1 and centre_letter in pū.consonants:
        #3 squares remaining

        #get the *empty square in the middle row*
        if digraph1_squares == (0,1) : empty_square_middle_row = 3
        if digraph1_squares == (1,2) : empty_square_middle_row = 7
        if digraph1_squares == (6,5) : empty_square_middle_row = 3
        if digraph1_squares == (5,4) : empty_square_middle_row = 7

        #the *empty square in the middle row* must have a vowel in it
        letter_to_place = random.choice([x for x in single_letters if x in pū.all_vowels])
        single_letters.remove(letter_to_place)
        koru[empty_square_middle_row] = letter_to_place #2 squares remaining

        #fill the remaining 2 squares with whatever letters remain
        for index, square in enumerate(koru):
            if square is None:
                letter_to_place = random.choice(single_letters)
                single_letters.remove(letter_to_place)
                koru[index] = letter_to_place


    if digraphs_count == 1 and centre_letter in pū.all_vowels:
        #3 squares remaining (1 isolated and 2 vertically together)
        #3C or 2C, 1V or 1C, 2V

        #mostly these will be 3 consonants and we just want to ensure that we
        #don't create any 'vertical digraphs'
        #and we want to keep vowels and consonants separate

        #get the *isolated empty square*
        if digraph1_squares == (0,1) : isolated_empty_square = 6
        if digraph1_squares == (1,2) : isolated_empty_square = 4
        if digraph1_squares == (6,5) : isolated_empty_square = 0
        if digraph1_squares == (5,4) : isolated_empty_square = 2

        #the *isolated empty square* must have a 'w' in it if we have one
        #otherwise a consonant
        if 'w' in single_letters:
            letter_to_place = 'w'
        else:
            letter_to_place = random.choice([x for x in single_letters if x in pū.consonants])
            
        single_letters.remove(letter_to_place)
        koru[isolated_empty_square] = letter_to_place #2 squares remaining

        #get the *empty square in the middle row*
        if digraph1_squares == (0,1) : empty_square_middle_row = 3
        if digraph1_squares == (1,2) : empty_square_middle_row = 7
        if digraph1_squares == (6,5) : empty_square_middle_row = 3
        if digraph1_squares == (5,4) : empty_square_middle_row = 7

        #the *empty square in the middle row* must have a consonant in it if we 
        #have one otherwise a vowel.
        try:
            letter_to_place = random.choice([x for x in single_letters if x in pū.consonants])
        except IndexError:
            #no consonants remaining
            letter_to_place = random.choice([x for x in single_letters if x in pū.all_vowels])    

        single_letters.remove(letter_to_place)
        koru[empty_square_middle_row] = letter_to_place #1 square remaining

        #fill the remaining square with whatever letter remains
        for index, square in enumerate(koru):
            if square is None:
                letter_to_place = random.choice(single_letters)
                single_letters.remove(letter_to_place)
                koru[index] = letter_to_place
    #DONE for 1 digraph

    if digraphs_count == 0:
        #no digraphs, so only the centre letter has been placed
        #we have 8 letters left to place
        if centre_letter in pū.all_vowels:
            vowel_first = True
        else:
            vowel_first = False
        for index, square in enumerate(koru[:-1]):
            if index % 2 == 0: #0, 2, 4, 6
                if vowel_first:
                    letter_to_place = random.choice([x for x in single_letters \
                                                        if x in pū.all_vowels])
                else:
                    try:
                        letter_to_place = random.choice([x for x in single_letters \
                                                            if x in pū.consonants])
                    except IndexError:
                        #no consonants remaining
                        letter_to_place = random.choice([x for x in single_letters \
                                                            if x in pū.all_vowels])
            else: #1, 3, 5, 7
                if vowel_first:
                    try:
                        letter_to_place = random.choice([x for x in single_letters \
                                                            if x in pū.consonants])
                    except IndexError:
                        #no consonants remaining
                        letter_to_place = random.choice([x for x in single_letters \
                                                            if x in pū.all_vowels])
                else:
                    letter_to_place = random.choice([x for x in single_letters \
                                                        if x in pū.all_vowels])
            single_letters.remove(letter_to_place)
            koru[index] = letter_to_place   
#DONE for 0 digraphs
    print(seed_word, koru)



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
    #get_nines_structure_parser = subparsers.add_parser('get_nines_structure')
    #get_nines_structure_parser.set_defaults(function = get_nines_structure)

    # create the parser for the get_seed_word_structure function
    get_seed_word_structure_parser = subparsers.add_parser('get_seed_word_structure')
    get_seed_word_structure_parser.add_argument('-seed_word')
    get_seed_word_structure_parser.set_defaults(function = get_seed_word_structure)

    # create the parser for the get_koru function
    get_koru_parser = subparsers.add_parser('get_koru')
    get_koru_parser.add_argument('-seed_word')
    get_koru_parser.set_defaults(function = get_koru)

    # create the parser for the get_nines_subset function
    get_nines_subset_parser = subparsers.add_parser('get_nines_subset')
    get_nines_subset_parser.set_defaults(function = get_nines_subset)

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
