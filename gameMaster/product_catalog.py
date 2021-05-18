# These dictionaries define how many of a certain product is associated with a certain product number.
catalog = {
    # Spicy McChicken
    'spicy_chicken': {
        'names': {
            'lower': 'Spicy McChicken',
            'lower_plural': 'Spicy McChicken',
            'upper': 'SPICY McCHICKEN',
            'upper_plural': 'SPICY McCHICKEN'
        },
        'codes': {
            '14329': 1,  # Hab
            '14330': 1,  # Hab VM
            '14809': 1,  # Hab Reg
            '16510': 1,  # Szech
            '16513': 1,  # Szech EVM

        },
        'level_exclusion': False,
        'footer': '💬 &quot;Would you like to make that a spicy McChicken today?&quot; 🔥'
    },

    # DONUT
    'donut': {
        'names': {
            'lower': 'donut',
            'lower_plural': 'donuts',
            'upper': 'DONUT',
            'upper_plural': 'DONUTS'
        },
        'codes': {
            '16347': 12,
            # '15194': 12,
            # '16344': 6,
            '15191': 6,
            # '15188': 2,
            '15197': 1,
            '15202': 1,
            '15367': 1,
            '15212': 1,
            '15217': 1,
            '16409': 1   # CINNAMON CREAM DONUT
            },
        'level_exclusion': False,
        'footer': '🍩 Two donuts: <b>$1.49</b> &nbsp&nbsp 💡 Buy one, get one 50% off! &nbsp&nbsp 💬 &quot;Would you like two donuts for $1.49?&quot;'
    },

    #FRY
    'fry': {
        'names': {
            'lower': 'large fry',
            'lower_plural': 'large fries',
            'upper': 'LARGE FRY',
            'upper_plural': 'LARGE FRIES'
        },
        'codes': {
            '239': 1,
            '13525': 1,
            '13524': 1,
            '11811': 1,
            '13526': 1
            },

        'level_exclusion': False,
        'footer': '🍟 Upsize cost: <b>60¢</b> &nbsp&nbsp 💬 &quot;Would you like to upgrade to a large fry for 60¢?&quot;'


        },

    # FRIES FOR RMHC
    'rmhc_fry': {
        'names': {
            'lower': 'RMHC fry',
            'lower_plural': 'RMHC fries',
            'upper': 'RMHC FRY',
            'upper_plural': 'RMHCAd FRIES'
        },
        'codes': {
            '12': 1,     # M FRY
            '11810': 1,  # M FRY RV
            '239': 1,    # L FRY
            '13525': 1,  # POUTINE OPT VM
            '13524': 1,  # POUTINE OPT
            '11811': 1,  # L FRY RV
            '13526': 1   # POUTINE OPT RV
            },

        'level_exclusion': False,
        'footer': '&#128106; &#127969; McDonald\'s will donate a portion of proceeds to RMHC Atlantic! &#127839; &#128149;'


        },

    #PIE
    'pie': {
        'names': {
            'lower': 'pie',
            'lower_plural': 'pie',
            'upper': 'PIE',
            'upper_plural': 'PIES'
        },
        'codes': {
            '1054': 2,
            '352': 1
            },
        'level_exclusion': False,
        'footer': '🥧 Upsize cost: <b>50¢</b> &nbsp&nbsp 💬 &quot;Would you like some apple pies to complete your order today?&quot;'
        },

    #HASH BROWN
    'hashbrown': {
        'names': {
            'lower': 'hash brown',
            'lower_plural': 'hash browns',
            'upper': 'HASH BROWN',
            'upper_plural': 'HASH BROWNS'
        },
        'codes': {
            '12082': 2,
            '10540': 2,
            '35': 1,
            '12081': 1
            },
        'level_exclusion': False,
        'footer': '🔔 Upsize cost: <b>$1</b> &nbsp&nbsp 💬 &quot;Would you like an extra hash brown to go with your meal?&quot;'
        },

    #MUFFIN
    'muffin': {
        'names': {
            'lower': 'muffin',
            'lower_plural': 'muffins',
            'upper': 'MUFFIN',
            'upper_plural': 'MUFFINS'
        },
        'codes': {
            # '9900': 6,      # 6 Pack ( Keep an eye on potential level_exclusion bug. )
            '10741': 1,     # Banana
            '10742': 1,     # Banana VM
            '11777': 1,     # Blueberry VM
            '11776': 1,     # Blueberry
            '11936': 1,     # Carrot
            '11937': 1,     # Carrot VM
            '11938': 1,     # Cranberry
            '11939': 1,     # Cranberry VM
            '11778': 1,     # Fruit
            '11779': 1      # Fruit VM
            },
        'level_exclusion': False,
        'footer': '🧁 Pairing cost: <b>70¢</b> &nbsp&nbsp 💬 &quot;Would you like a muffin to go with your coffee for 70¢?&quot;'
        },

    # COOKIE
    'cookie': {
        'names': {
            'lower': 'cookie',
            'lower_plural': 'cookies',
            'upper': 'COOKIE',
            'upper_plural': 'COOKIES'
        },
        'codes': {
            # '13913': 12,  # 12 cookies
            # '13912': 6,  # 6 cookies
            # '13911': 2,  # 2 cookies
            '13908': 1,  # Chocolate chunk
            '14870': 1,  # Brownie
        },
        'level_exclusion': False,
        'footer': '🍪 Two cookies: <b>$1.49</b> &nbsp&nbsp 💡 Buy one, get one 50% off! &nbsp&nbsp 💬 &quot;Would you like two cookies for $1.49?&quot;'
    },

    # COFFEE
    'coffee': {
        'names': {
            'lower': 'coffee',
            'lower_plural': 'coffee',
            'upper': 'COFFEE',
            'upper_plural': 'COFFEE'
        },
        'codes': {
            '2613': 1,   # L coffee
            '11627': 1,  # XL coffee
            '13464': 1,  # L senior
            '13465': 1,  # XL senior
            '2622': 1,   # L coffee R
            '11628': 1,  # XL coffee R
        },
        'level_exclusion': False,
        'footer': '🍪 Two cookies: <b>$1.49</b> &nbsp&nbsp 💡 Buy one, get one 50% off! &nbsp&nbsp 💬 &quot;Would you like two cookies for $1.49?&quot;'
    },
    }
