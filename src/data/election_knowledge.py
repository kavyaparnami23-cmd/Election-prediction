"""
Author      : Kavya Parnami
Project     : ElectionPulse AI
Description : Real election knowledge base using 2019 and 2024 Lok Sabha results.
              Used in predict_party_contest to replace hash-based bias.
"""

# ─────────────────────────────────────────────────────────────
# 2024 Lok Sabha — Direct constituency winner lookup
# Key = constituency name (lowercase, stripped)
# Value = winning party abbreviation
# ─────────────────────────────────────────────────────────────

CONSTITUENCY_2024 = {
    # ── Gujarat (BJP 25/26) ──────────────────────────────────
    'gandhinagar':            'BJP',
    'ahmedabad east':         'BJP',
    'ahmedabad west':         'BJP',
    'sabarkantha':            'BJP',
    'banaskantha':            'Congress',  # Congress's only Gujarat seat
    'patan':                  'BJP',
    'mahesana':               'BJP',
    'surendranagar':          'BJP',
    'rajkot':                 'BJP',
    'amreli':                 'BJP',
    'junagadh':               'BJP',
    'porbandar':              'BJP',
    'jamnagar':               'BJP',
    'kutch':                  'BJP',
    'anand':                  'BJP',
    'kheda':                  'BJP',
    'vadodara':               'BJP',
    'navsari':                'BJP',
    'valsad':                 'BJP',
    'surat':                  'BJP',
    'bardoli':                'BJP',
    'bharuch':                'BJP',
    'bhavnagar':              'BJP',

    # ── Madhya Pradesh (BJP 29/29) ───────────────────────────
    'bhopal':                 'BJP',
    'indore':                 'BJP',
    'gwalior':                'BJP',
    'jabalpur':               'BJP',
    'ujjain':                 'BJP',
    'vidisha':                'BJP',
    'sagar':                  'BJP',
    'rewa':                   'BJP',
    'satna':                  'BJP',
    'damoh':                  'BJP',
    'khajuraho':              'BJP',
    'tikamgarh':              'BJP',
    'morena':                 'BJP',
    'rajgarh':                'BJP',

    # ── Delhi (BJP 7/7) ──────────────────────────────────────
    'chandni chowk':          'BJP',
    'north east delhi':       'BJP',
    'east delhi':             'BJP',
    'new delhi':              'BJP',
    'north west delhi':       'BJP',
    'west delhi':             'BJP',
    'south delhi':            'BJP',

    # ── Uttarakhand (BJP 5/5) ────────────────────────────────
    'haridwar':               'BJP',
    'tehri garhwal':          'BJP',
    'pauri garhwal':          'BJP',
    'almora':                 'BJP',
    'nainital-udhamsingh nagar': 'BJP',

    # ── Odisha (BJP 20/21) ───────────────────────────────────
    'bhubaneswar':            'BJP',
    'cuttack':                'BJP',
    'puri':                   'BJP',
    'sambalpur':              'BJP',
    'berhampur':              'Congress',

    # ── Chhattisgarh (BJP 10/11) ─────────────────────────────
    'raipur':                 'BJP',
    'bilaspur':               'BJP',
    'durg':                   'BJP',
    'korba':                  'Congress',

    # ── Rajasthan (BJP 14, Congress 8, others 3) ─────────────
    'jaipur':                 'BJP',
    'jaipur rural':           'BJP',
    'sikar':                  'Congress',
    'jhunjhunu':              'Congress',
    'alwar':                  'BJP',
    'bharatpur':              'BJP',
    'karauli-dholpur':        'BJP',
    'dausa':                  'BJP',
    'tonk-sawai madhopur':    'Congress',
    'ajmer':                  'BJP',
    'nagaur':                 'Congress',
    'jodhpur':                'Congress',
    'barmer':                 'Congress',
    'jalore':                 'BJP',
    'udaipur':                'BJP',
    'chittorgarh':            'BJP',
    'bhilwara':               'BJP',
    'kota':                   'BJP',
    'baran-jhalawar':         'BJP',
    'bikaner':                'BJP',
    'ganganagar':             'BJP',
    'churu':                  'BJP',
    'pali':                   'BJP',
    'banswara':               'BJP',

    # ── Karnataka (BJP 17, Congress 9, JD(S) 2) ──────────────
    'bengaluru south':        'BJP',
    'bengaluru north':        'BJP',
    'bengaluru central':      'BJP',
    'bengaluru rural':        'Congress',
    'mysore':                 'BJP',
    'mangalore':              'BJP',
    'udupi chikmagalur':      'BJP',
    'hassan':                 'JD(S)',
    'mandya':                 'JD(S)',
    'tumkur':                 'Congress',
    'chikkaballapur':         'Congress',
    'kolar':                  'Congress',
    'chitradurga':            'BJP',
    'davangere':              'BJP',
    'shimoga':                'BJP',
    'hubli dharwad':          'BJP',
    'dharwad':                'BJP',
    'gadag':                  'BJP',
    'haveri':                 'BJP',
    'belagavi':               'BJP',
    'bijapur':                'BJP',
    'bagalkot':               'BJP',
    'koppal':                 'BJP',
    'raichur':                'BJP',
    'bellary':                'Congress',
    'bidar':                  'Congress',
    'gulbarga':               'Congress',

    # ── Kerala (Congress/UDF 18, CPI(M) 1, BJP 1) ────────────
    'thiruvananthapuram':     'Congress',
    'attingal':               'Congress',
    'kollam':                 'Congress',
    'pathanamthitta':         'Congress',
    'alappuzha':              'Congress',
    'kottayam':               'Congress',
    'idukki':                 'Congress',
    'ernakulam':              'Congress',
    'thrissur':               'BJP',       # BJP's only Kerala seat (2024)
    'chalakudy':              'Congress',
    'palakkad':               'Congress',
    'malappuram':             'IUML',
    'ponnani':                'IUML',
    'kozhikode':              'Congress',
    'wayanad':                'Congress',
    'vadakara':               'Congress',
    'kannur':                 'CPI(M)',
    'kasargod':               'Congress',

    # ── Tamil Nadu (DMK alliance 39/39) ──────────────────────
    'chennai north':          'DMK',
    'chennai south':          'Congress',
    'chennai central':        'DMK',
    'vellore':                'DMK',
    'coimbatore':             'DMK',
    'madurai':                'DMK',
    'thanjavur':              'Congress',
    'tiruchirappalli':        'DMK',
    'tirunelveli':            'Congress',
    'dindigul':               'DMK',
    'erode':                  'Congress',
    'nilgiris':               'DMK',
    'salem':                  'DMK',
    'namakkal':               'DMK',
    'krishnagiri':            'DMK',
    'dharmapuri':             'DMK',
    'vellore':                'DMK',
    'arani':                  'DMK',
    'tiruvallur':             'DMK',
    'kancheepuram':           'DMK',
    'chengalpattu':           'Congress',
    'sriperumbudur':          'DMK',
    'cuddalore':              'DMK',
    'tenkasi':                'DMK',
    'thoothukudi':            'Congress',
    'ramanathapuram':         'DMK',
    'sivaganga':              'Congress',
    'viluppuram':             'VCK',
    'kallakurichi':           'DMK',
    'nagapattinam':           'DMK',
    'mayiladuthurai':         'Congress',
    'theni':                  'AIADMK',

    # ── Uttar Pradesh (BJP 33, SP 37, Congress 6, others) ────
    'varanasi':               'BJP',
    'lucknow':                'BJP',
    'amethi':                 'Congress',  # Congress won back in 2024
    'rae bareli':             'Congress',  # Rahul Gandhi won
    'kanpur':                 'BJP',
    'allahabad':              'BJP',
    'gorakhpur':              'BJP',
    'agra':                   'BJP',
    'mathura':                'BJP',
    'aligarh':                'BJP',
    'ghaziabad':              'BJP',
    'gautam buddha nagar':    'BJP',
    'meerut':                 'BJP',
    'faizabad':               'SP',        # Ayodhya — SP won despite Ram Mandir
    'azamgarh':               'SP',
    'mainpuri':               'SP',
    'firozabad':              'SP',
    'etawah':                 'BJP',
    'moradabad':              'SP',
    'bareilly':               'BJP',
    'pilibhit':               'BJP',
    'shahjahanpur':           'BJP',
    'unnao':                  'BJP',
    'sitapur':                'SP',
    'hardoi':                 'BJP',
    'misrikh':                'BJP',
    'lakhimpur kheri':        'BJP',
    'sultanpur':              'BJP',
    'pratapgarh':             'SP',
    'jaunpur':                'SP',
    'sant kabir nagar':       'BJP',
    'basti':                  'BJP',
    'ghazipur':               'SP',
    'ballia':                 'BJP',
    'jhansi':                 'BJP',
    'hamirpur':               'BJP',
    'banda':                  'BJP',

    # ── Maharashtra (2024 — post-split factions) ───────────────────────
    # NDA (MahaYuti): BJP + Shiv Sena (Shinde) + NCP (Ajit)
    # INDIA (MVA):    Congress + Shiv Sena (UBT) + NCP (SP)
    'mumbai north':           'BJP',
    'mumbai north west':      'ShivSena(Shinde)',   # Ravindra Waikar
    'mumbai north east':      'ShivSena(Shinde)',
    'mumbai north central':   'Congress',           # Varsha Gaikwad (MVA)
    'mumbai south central':   'Congress',
    'mumbai south':           'ShivSena(UBT)',      # Arvind Sawant
    'pune':                   'BJP',
    'nashik':                 'ShivSena(Shinde)',   # Hemant Godse
    'thane':                  'ShivSena(Shinde)',   # Naresh Mhaske
    'kalyan':                 'ShivSena(Shinde)',
    'baramati':               'NCP(SP)',            # Supriya Sule
    'shirdi':                 'ShivSena(Shinde)',
    'buldhana':               'ShivSena(Shinde)',
    'hatkanangle':            'ShivSena(Shinde)',
    'raigad':                 'ShivSena(UBT)',
    'bhiwandi':               'ShivSena(UBT)',
    'madha':                  'ShivSena(UBT)',
    'maval':                  'BJP',
    'akola':                  'BJP',
    'ratnagiri-sindhudurg':   'BJP',
    'palghar':                'BJP',
    'satara':                 'Congress',
    'kolhapur':               'Congress',
    'sangli':                 'Congress',
    'solapur':                'BJP',
    'ahmednagar':             'BJP',
    'amravati':               'Congress',
    'nagpur':                 'BJP',
    'aurangabad':             'AIMIM',
    'nanded':                 'Congress',

    # ── Haryana (BJP 5, Congress 5) ──────────────────────────
    'gurugram':               'BJP',
    'faridabad':              'BJP',
    'rohtak':                 'Congress',
    'ambala':                 'Congress',
    'kurukshetra':            'BJP',
    'hisar':                  'Congress',
    'bhiwani-mahendragarh':   'BJP',
    'sonipat':                'Congress',
    'karnal':                 'BJP',

    # ── Punjab (Congress 7, AAP 3, BJP 2, Akali 1) ───────────
    'amritsar':               'Congress',
    'ludhiana':               'Congress',
    'jalandhar':              'AAP',
    'patiala':                'Congress',
    'gurdaspur':              'BJP',
    'anandpur sahib':         'AAP',
    'hoshiarpur':             'Congress',
    'fatehgarh sahib':        'AAP',
    'firozpur':               'BJP',
    'bathinda':               'Akali',
    'sangrur':                'AAP',

    # ── Bihar (NDA wins big: BJP 12, JD(U) 12, LJP 5) ───────
    'patna sahib':            'BJP',
    'pataliputra':            'BJP',
    'muzaffarpur':            'BJP',
    'gaya':                   'BJP',
    'darbhanga':              'BJP',
    'madhubani':              'BJP',
    'sitamarhi':              'BJP',

    # ── West Bengal (TMC 29, BJP 12, Congress 1) ─────────────
    'kolkata north':          'TMC',
    'kolkata south':          'TMC',
    'jadavpur':               'TMC',
    'diamond harbour':        'TMC',
    'howrah':                 'TMC',
    'asansol':                'TMC',
    'bardhaman purba':        'TMC',
    'bardhaman-durgapur':     'BJP',
    'darjeeling':             'BJP',
    'coochbehar':             'BJP',
    'bankura':                'BJP',
    'bishnupur':              'BJP',
    'purulia':                'BJP',

    # ── Himachal Pradesh (Congress 3, BJP 1) ─────────────────
    'shimla':                 'BJP',
    'mandi':                  'Congress',
    'hamirpur':               'BJP',
    'kangra':                 'BJP',

    # ── Telangana (Congress 8, BJP 8, AIMIM 1) ───────────────
    'secunderabad':           'BJP',
    'malkajgiri':             'Congress',
    'medak':                  'BJP',
    'karimnagar':             'BJP',
    'nizamabad':              'Congress',
    'adilabad':               'BJP',
    'warangal':               'Congress',
    'nalgonda':               'Congress',
    'hyderabad':              'AIMIM',
    'mahabubabad':            'Congress',
    'khammam':                'BJP',
    'bhongir':                'Congress',

    # ── Andhra Pradesh (TDP alliance, YSRCP routed) ──────────
    'visakhapatnam':          'TDP',
    'vijayawada':             'TDP',
    'guntur':                 'TDP',
    'tirupati':               'TDP',
    'nellore':                'TDP',
    'rajampet':               'TDP',
    'kurnool':                'TDP',
    'nandyal':                'TDP',

    # ── Jharkhand ────────────────────────────────────────────
    'ranchi':                 'BJP',
    'dhanbad':                'BJP',
    'jamshedpur':             'BJP',
    'hazaribagh':             'BJP',

    # ── Assam (BJP alliance 11, Congress 2, AIUDF 1) ─────────
    'guwahati':               'BJP',
    'dibrugarh':              'BJP',
    'jorhat':                 'BJP',
    'tezpur':                 'BJP',
    'silchar':                'BJP',
    'autonomous district':    'Congress',
    'kaziranga':              'BJP',
    'sonitpur':               'BJP',
    'lakhimpur':              'BJP',
}

# ─────────────────────────────────────────────────────────────
# 2019 Lok Sabha — Direct constituency winner lookup
# ─────────────────────────────────────────────────────────────

CONSTITUENCY_2019 = {
    # Famously contested seats
    'varanasi':               'BJP',
    'gandhinagar':            'BJP',
    'amethi':                 'BJP',     # Smriti Irani won
    'rae bareli':             'Congress',
    'wayanad':                'Congress',
    'faizabad':               'BJP',     # BJP held it in 2019
    'lucknow':                'BJP',
    'bhopal':                 'BJP',
    'indore':                 'BJP',
    'new delhi':              'BJP',
    'ahmedabad east':         'BJP',
    'ahmedabad west':         'BJP',
    'surat':                  'BJP',
    'vadodara':               'BJP',
    'mumbai north':           'BJP',
    'pune':                   'BJP',
    'kolkata north':          'TMC',
    'kolkata south':          'TMC',
    'jadavpur':               'TMC',
    'hyderabad':              'AIMIM',
    'thrissur':               'Congress',  # Congress held it in 2019
    'patna sahib':            'BJP',
    'nagpur':                 'BJP',
    'chennai north':          'DMK',
    'tirupati':               'YSRCP',
}

# ─────────────────────────────────────────────────────────────
# Detailed per-party seat data by state — 2024 Lok Sabha
# Key = lowercase normalised party name
# Much more accurate than (bjp, congress, total) tuples
# ─────────────────────────────────────────────────────────────

STATE_PARTY_SEATS_2024: dict[str, dict] = {
    'Tamil Nadu':       {'dmk':22,'congress':9,'vck':2,'cpi':2,'cpm':2,'mdmk':1,'aiadmk':0,'bjp':0,'tvk':0,'total':39},
    'Uttar Pradesh':    {'bjp':33,'sp':37,'congress':6,'rld':2,'bsp':0,'total':80},
    'Maharashtra':      {'bjp':9,'congress':13,'shivsena(ubt)':9,'ncp(sp)':8,'shivsena(shinde)':7,'ncp(ajit)':1,'aimim':1,'total':48},
    'West Bengal':      {'tmc':29,'bjp':12,'congress':1,'total':42},
    'Bihar':            {'bjp':12,'jdu':12,'ljp':5,'congress':3,'rjd':4,'cpi(ml)':3,'ham':1,'total':40},
    'Kerala':           {'congress':18,'bjp':1,'iuml':2,'cpi(m)':1,'total':20},
    'Andhra Pradesh':   {'tdp':16,'bjp':3,'jsp':2,'ysrcp':4,'total':25},
    'Telangana':        {'bjp':8,'congress':8,'aimim':1,'total':17},
    'Karnataka':        {'bjp':17,'congress':9,'jd(s)':2,'total':28},
    'Rajasthan':        {'bjp':14,'congress':8,'rld':1,'total':25},
    'Gujarat':          {'bjp':25,'congress':1,'total':26},
    'Madhya Pradesh':   {'bjp':29,'total':29},
    'Odisha':           {'bjp':20,'congress':1,'total':21},
    'Jharkhand':        {'bjp':8,'congress':2,'jmm':3,'cpi(ml)':1,'total':14},
    'Punjab':           {'congress':7,'aap':3,'bjp':2,'akali dal':1,'total':13},
    'Haryana':          {'bjp':5,'congress':5,'total':10},
    'Delhi':            {'bjp':7,'total':7},
    'Assam':            {'bjp':9,'congress':3,'aiudf':1,'agp':1,'total':14},
    'Uttarakhand':      {'bjp':5,'total':5},
    'Himachal Pradesh': {'bjp':2,'congress':2,'total':4},
    'Chhattisgarh':     {'bjp':10,'congress':1,'total':11},
    'Arunachal Pradesh':{'bjp':2,'total':2},
    'Manipur':          {'bjp':2,'total':2},
    'Tripura':          {'bjp':2,'total':2},
    'Goa':              {'bjp':2,'total':2},
    'Meghalaya':        {'bjp':1,'congress':1,'total':2},
    'Jammu & Kashmir':  {'nc':2,'congress':1,'bjp':2,'total':5},
}

STATE_PARTY_SEATS_2019: dict[str, dict] = {
    'Tamil Nadu':       {'bjp':1,'aiadmk':1,'dmk':22,'congress':8,'total':39},
    'Uttar Pradesh':    {'bjp':62,'sp':5,'congress':1,'bsp':10,'rld':0,'total':80},
    'Maharashtra':      {'bjp':23,'congress':1,'shivsena':18,'ncp':4,'total':48},
    'West Bengal':      {'tmc':22,'bjp':18,'congress':2,'total':42},
    'Bihar':            {'bjp':17,'jdu':16,'ljp':6,'congress':1,'rjd':0,'total':40},
    'Kerala':           {'congress':15,'bjp':0,'iuml':2,'cpi(m)':3,'total':20},
    'Andhra Pradesh':   {'ysrcp':22,'tdp':3,'total':25},
    'Telangana':        {'bjp':4,'congress':3,'trs':9,'aimim':1,'total':17},
    'Karnataka':        {'bjp':25,'congress':1,'jds':1,'total':28},
    'Gujarat':          {'bjp':26,'total':26},
    'Madhya Pradesh':   {'bjp':28,'congress':1,'total':29},
    'Rajasthan':        {'bjp':24,'congress':1,'total':25},
    'Punjab':           {'congress':8,'bjp':2,'akali dal':2,'aap':1,'total':13},
    'Assam':            {'bjp':9,'congress':3,'aiudf':1,'total':14},
    'Jharkhand':        {'bjp':11,'congress':1,'jmm':1,'total':14},
    'Haryana':          {'bjp':10,'congress':0,'total':10},
    'Delhi':            {'bjp':7,'total':7},
}

# ─────────────────────────────────────────────────────────────
# Geography penalty: regional parties get near-zero score
# when they contest outside their home state(s).
# National parties (BJP, Congress, AAP, BSP, CPI, CPM)
# are NOT listed here — they contest everywhere.
# ─────────────────────────────────────────────────────────────

PARTY_HOME_STATES: dict[str, list[str]] = {
    # Uttar Pradesh belt
    'sp':                  ['Uttar Pradesh'],
    'bsp':                 ['Uttar Pradesh', 'Madhya Pradesh', 'Rajasthan'],
    'rld':                 ['Uttar Pradesh', 'Haryana'],
    # Bengal
    'tmc':                 ['West Bengal', 'Tripura'],
    # Tamil Nadu
    'dmk':                 ['Tamil Nadu'],
    'aiadmk':              ['Tamil Nadu'],
    'tvk':                 ['Tamil Nadu'],   # TVK (actor Vijay) — TN only
    'vck':                 ['Tamil Nadu'],
    'mdmk':                ['Tamil Nadu'],
    'iuml':                ['Kerala', 'Tamil Nadu'],
    # Telangana / AP
    'trs/brs':             ['Telangana'],
    'brs':                 ['Telangana'],
    'ysrcp':               ['Andhra Pradesh'],
    'tdp':                 ['Andhra Pradesh'],
    'jsp':                 ['Andhra Pradesh'],
    # Bihar / Jharkhand
    'rjd':                 ['Bihar'],
    'jdu':                 ['Bihar'],
    'ljp':                 ['Bihar'],
    'ham':                 ['Bihar'],
    'jmm':                 ['Jharkhand'],
    # Odisha
    'bjd':                 ['Odisha'],
    # Assam
    'agp':                 ['Assam'],
    'aiudf':               ['Assam'],
    # Maharashtra
    'shivsena(shinde)':    ['Maharashtra'],
    'shivsena(ubt)':       ['Maharashtra'],
    'shivsena':            ['Maharashtra'],
    'ncp(sp)':             ['Maharashtra'],
    'ncp(ajit)':           ['Maharashtra'],
    'ncp':                 ['Maharashtra'],
    # Multi-state / specific
    'aimim':               ['Telangana', 'Maharashtra', 'Bihar'],
    'nc':                  ['Jammu & Kashmir'],
    'pdp':                 ['Jammu & Kashmir'],
    'akali dal':           ['Punjab'],
    'jd(s)':               ['Karnataka'],
    'jds':                 ['Karnataka'],
}


def get_party_win_probability(party1: str, party2: str,
                               state: str, constituency: str = '') -> tuple[float, float]:
    """
    Returns (prob1, prob2) — head-to-head win probability.

    Data sources (in priority order):
      1. 2024 constituency winner        (weight 3.0)
      2. 2019 constituency winner        (weight 1.5)
      3. Detailed 2024 state seat share  (weight 1.2 × geo_multiplier)
      4. Detailed 2019 state seat share  (weight 0.5 × geo_multiplier)

    Geography multiplier:
      - National parties (BJP, Congress, etc.) → 1.0 everywhere
      - Regional parties outside home state   → 0.03 (97% penalty)
    """
    p1_lower = party1.strip().lower()
    p2_lower = party2.strip().lower()
    c_key    = constituency.strip().lower()

    # ── normalise: remove brackets/spaces for lookups ────────────
    def norm(s: str) -> str:
        return s.replace('(', '').replace(')', '').replace(' ', '')

    # ── Geography multiplier ─────────────────────────────────────
    def geo_mult(party_lower: str) -> float:
        home = PARTY_HOME_STATES.get(norm(party_lower)) or PARTY_HOME_STATES.get(party_lower)
        if home is None:
            return 1.0   # national party — no penalty
        return 1.0 if state in home else 0.03

    gm1 = geo_mult(p1_lower)
    gm2 = geo_mult(p2_lower)

    # ── _match: fuzzy party name matching ────────────────────────
    def _match(winner_str: str | None, party_lower: str) -> bool:
        if not winner_str:
            return False
        w = norm(winner_str.lower())
        p = norm(party_lower)

        if w == p:
            return True

        # Shiv Sena factions
        def is_shinde(s): return 'shinde' in s or 'eknath' in s
        def is_ubt(s):    return 'ubt' in s or 'uddhav' in s
        def is_ss(s):     return 'shivsena' in s

        if p in ('shivsena', 'ss'):
            return is_ss(w)
        if 'shinde' in p or p == 'shivsenashinde':
            return is_shinde(w) or (is_ss(w) and not is_ubt(w))
        if 'ubt' in p or p == 'shivsenaubt':
            return is_ubt(w) or (is_ss(w) and not is_shinde(w))

        # NCP factions
        if p in ('ncp',):
            return 'ncp' in w
        if 'sp' in p and 'ncp' in p:
            return 'ncpsp' in w or (w == 'ncp') or ('ncp' in w and 'sp' in w)
        if 'ajit' in p and 'ncp' in p:
            return 'ncpajit' in w or (w == 'ncp') or ('ncp' in w and 'ajit' in w)

        # Common aliases (extended for new parties)
        ALIASES: dict[str, set[str]] = {
            'congress': {'inc', 'congress', 'udf'},
            'bjp':      {'bjp'},
            'sp':       {'sp', 'samajwadi'},
            'tmc':      {'tmc', 'trinamool', 'aitc'},
            'dmk':      {'dmk'},
            'aiadmk':   {'aiadmk'},
            'tvk':      {'tvk'},        # Tamilaga Vettri Kazhagam
            'vck':      {'vck'},        # Viduthalai Chiruthaigal Katchi
            'tdp':      {'tdp', 'telugudesam'},
            'ysrcp':    {'ysrcp', 'ysrcongress'},
            'jsp':      {'jsp', 'janasena'},
            'jdu':      {'jdu'},
            'ljp':      {'ljp', 'lokjanshakti'},
            'rld':      {'rld'},
            'rjd':      {'rjd'},
            'jmm':      {'jmm'},
            'trs/brs':  {'trs', 'brs'},
            'brs':      {'brs', 'trs'},
            'nc':       {'nc', 'nationalconference'},
            'aiudf':    {'aiudf'},
            'aimim':    {'aimim'},
            'aap':      {'aap'},
            'bjd':      {'bjd'},
            'agp':      {'agp'},
            'jds':      {'jds', 'jd(s)'},
            'akali dal':{'akali', 'shiromani'},
        }
        for canonical, alts in ALIASES.items():
            if canonical == p:
                return any(a in w for a in alts)

        return p in w or w in p

    # ── Compute detailed state seat share ─────────────────────────
    def detailed_share(party_lower: str, seats: dict) -> float:
        total = seats.get('total', 1) or 1
        p = norm(party_lower)

        # direct key match
        if p in seats:
            return seats[p] / total

        # alias map for lookup keys
        KEY_MAP = {
            'congress': 'congress', 'inc': 'congress',
            'bjp': 'bjp', 'sp': 'sp', 'bsp': 'bsp',
            'tmc': 'tmc', 'dmk': 'dmk', 'aiadmk': 'aiadmk', 'tvk': 'tvk',
            'vck': 'vck', 'ysrcp': 'ysrcp', 'tdp': 'tdp', 'jsp': 'jsp',
            'rjd': 'rjd', 'jdu': 'jdu', 'ljp': 'ljp', 'rld': 'rld',
            'jmm': 'jmm', 'bjd': 'bjd', 'aimim': 'aimim', 'aiudf': 'aiudf',
            'aap': 'aap', 'cpm': 'cpm', 'cpi': 'cpi', 'nc': 'nc',
            'agp': 'agp', 'akali dal': 'akali dal',
            'shivsena': 'shivsena', 'shivsena(shinde)': 'shivsena(shinde)',
            'shivsena(ubt)': 'shivsena(ubt)', 'ncp(sp)': 'ncp(sp)',
            'ncp(ajit)': 'ncp(ajit)', 'ncp': 'ncp',
            'trs': 'trs', 'brs': 'trs',
        }
        mapped = KEY_MAP.get(p) or KEY_MAP.get(party_lower)
        if mapped and mapped in seats:
            return seats[mapped] / total

        # partial key scan
        for k, v in seats.items():
            if k != 'total' and (k in p or p in k):
                return v / total

        return 0.0

    score1, score2 = 0.0, 0.0

    # ── 1. Constituency 2024 (weight 3.0) ────────────────────────
    w24 = CONSTITUENCY_2024.get(c_key)
    if w24:
        if _match(w24, p1_lower):
            score1 += 3.0
        elif _match(w24, p2_lower):
            score2 += 3.0
        else:
            score1 += 0.2
            score2 += 0.2

    # ── 2. Constituency 2019 (weight 1.5) ────────────────────────
    w19 = CONSTITUENCY_2019.get(c_key)
    if w19:
        if _match(w19, p1_lower):
            score1 += 1.5
        elif _match(w19, p2_lower):
            score2 += 1.5

    # ── 3. Detailed 2024 state seats (weight 1.2 × geo) ──────────
    seats24 = STATE_PARTY_SEATS_2024.get(state)
    if seats24:
        score1 += detailed_share(p1_lower, seats24) * 1.2 * gm1
        score2 += detailed_share(p2_lower, seats24) * 1.2 * gm2

    # ── 4. Detailed 2019 state seats (weight 0.5 × geo) ──────────
    seats19 = STATE_PARTY_SEATS_2019.get(state)
    if seats19:
        score1 += detailed_share(p1_lower, seats19) * 0.5 * gm1
        score2 += detailed_share(p2_lower, seats19) * 0.5 * gm2

    # ── Floor: no data found → apply geo multiplier to 0.5 base ─
    if score1 == 0.0 and score2 == 0.0:
        score1 = 0.5 * gm1
        score2 = 0.5 * gm2

    total_score = score1 + score2
    if total_score == 0:
        return 0.5, 0.5

    prob1 = round(min(0.97, max(0.03, score1 / total_score)), 4)
    prob2 = round(1.0 - prob1, 4)
    return prob1, prob2

