version = '1.9.0'
release = True
revision = ''

if release:
    fullVersion = '%s' % (version,)
else:
    fullVersion = '%s-%s' % (version, revision)

titleVersion = 'Version %s' % (fullVersion,)
