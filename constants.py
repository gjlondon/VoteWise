STATE_CHOICES = [
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming')
]
LIKERT_CHOICES = [
    ('1', 'Strongly Disagree'),
    ('2', 'Disagree'),
    ('3', 'Neutral'),
    ('4', 'Agree'),
    ('5', 'Strongly Agree')
]
LIKERT_LOOKUP = dict(LIKERT_CHOICES)
QUESTION_TEXT = {
    'housing': "Government intervention is necessary for affordable housing.",
    'economy': "Job creation is more important than wealth redistribution in California.",
    'environment': "Environmental protection is worth slowing economic growth in California.",
    'immigration': "California's resources should primarily serve its citizens, not undocumented immigrants.",
    'income_inequality': "Reducing income inequality is more important than promoting business growth in California.",
    'transportation': "Public transportation is more important than private vehicle infrastructure in California.",
    'education': "Public education funding is more important than tax cuts in California.",
    'healthcare': "A single-payer healthcare system is preferable to private healthcare in California.",
    'public_safety': "Community programs are more effective than traditional law enforcement in California.",
    'taxation': "Progressive taxation is more beneficial than lower taxes for all in California."
}

OAKLAND_MAYOR_CANDIDATES = ['Loren Manuel Taylor', 'Sheng Thao', 'Ignacio De La Fuente', 'Allyssa Victory Villanueva',
                            'Treva D. Reid', 'Gregory Hodge', 'Seneca Scott', 'John Reimann', 'Peter Y. Liu',
                            'Tyron C. Jordan']