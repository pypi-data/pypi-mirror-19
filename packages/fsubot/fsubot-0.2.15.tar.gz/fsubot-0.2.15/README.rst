FSUBot
======

A bot which serves as the foundation for other bots for use on the
Florida State University website. It is useful for automating tasks that
are otherwise very menial and tedious.


* How to start setting up commandline arguments:
    > fsu_dr = FSUBot(use_cli=True)
    > fsu_dr.setup(**fsu_dr.arg_parser.parse_args())
