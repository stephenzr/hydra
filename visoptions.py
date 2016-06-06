


class HeirarchyNoPhysics:
    def __init__(self):
        self.options = {
            'layout': {
                'hierarchical': {
                    'direction': "LR",
                    'sortMethod': "directed",
                    'nodeSpacing' : 165,
                }
            },
            'interaction': {'dragNodes': True},
            'physics': {
                'enabled':False
            }
        }

class LegalEntityOptions:
    def __init__(self):
        self.options = {
            'nodes' : {
                'shape': 'box'
            }
        }

class BigGraphOptions:
    def __init__(self):
        self.options = {
            'nodes': {
                'shape': 'dot',
                'scaling': {
                    'min': 10,
                    'max': 30,
                    'label': {
                        'min': 8,
                        'max': 30,
                        'drawThreshold': 12,
                        'maxVisible': 20
                    }
                },
                'font': {
                    'size': 16,
                    'face': 'Tahoma'
                }
            },
            'edges': {
                'width': 0.15,
                'color': {'inherit': 'from'},
                'smooth': {
                    'type': 'continuous'
                }
            },
            'physics': {
                'enabled':False
            },
            'interaction': {
                'tooltipDelay': 200,
                'hideEdgesOnDrag': True
            }
        }



