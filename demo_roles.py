class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


roles = {
    'User': (Permission.FOLLOW |
             Permission.COMMENT |
             Permission.WRITE_ARTICLES, True),
    'Moderator': (Permission.FOLLOW |
                  Permission.COMMENT |
                  Permission.WRITE_ARTICLES |
                  Permission.MODERATE_COMMENTS, False),
    'Administrator': (0xff, False)
}

per = roles['User'][0]
print(per)
