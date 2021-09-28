import logging
import logging.config
from flask_rest_experiment.app import create_app

if __name__ == '__main__':

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(name)s : %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            },
        },
        'loggers': {
            'flask_rest_experiment': {
                'handlers': ['default'],
                'level': 'DEBUG',
                'propagate': False,
            },
        }
    })
    logger = logging.getLogger('flask_rest_experiment')
    logger.info('starting application')

    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True)
