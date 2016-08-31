# suffix problems are caused either by
# incorrect data (mostly)

# or wrong programming assumptions 'tuai kerekeretanga'

# the format here is a dictionary with entries
# in the form

# (word_form) : (incorrect suffixes, correct suffixes)


suffix_problems = {}
suffix_problems['wawana'] = \
(('-', '-tanga', 'tanga', 'wananga'), 
('-tanga', 'wananga'))
suffix_problems['pēpē'] = \
(('-tanga', 'pēpētanga'), 
('-tanga',))
suffix_problems['tangi'] = \
(('-hanga', '-hia', '-nga', '-tia', 'hanga', 'hia'), 
('-hanga', '-hia', '-nga', '-tia'))
suffix_problems['tuai kerekere'] = \
(('kerekeretanga', 'tuai'),
('-tanga',))
suffix_problems['kauoroi'] = \
(('-hanga', '-hia', '-tanga', '-tia', 'hia'),
('-hanga', '-hia', '-tanga', '-tia'))
suffix_problems['kohi'] = \
(('-a', '-nga', 'nga'),
('-a', '-nga'))
suffix_problems['koto'] = \
(('-hanga', '-hia', '-nga', '-ngia', '-ranga', '-ria', '-tanga', '-tia', 'nga'),
('-hanga', '-hia', '-nga', '-ngia', '-ranga', '-ria', '-tanga', '-tia'))
suffix_problems['kō'] = \
(('-ia', '-nga', '-tanga', 'tia'),
('-ia', '-nga', '-tanga'))
suffix_problems['papahāro'] = \
(('tanga',),
('-tanga',))
suffix_problems['pipiha'] = \
(('-pihanga', '-tanga'),
('-tanga', 'pihanga'))
suffix_problems['pupuke'] = \
(('-nga', '-pukenga', '-tanga'),
('-nga', '-tanga', 'pukenga'))
suffix_problems['korite'] = \
(('-nga', '-tanga', 'hanga'),
('-hanga', '-nga', '-tanga'))
