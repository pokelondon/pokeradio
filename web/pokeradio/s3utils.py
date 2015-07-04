from storages.backends.s3boto import S3BotoStorage


class MediaRootS3BotoStorage(S3BotoStorage):
    location = ''
    host = 's3-eu-west-1.amazonaws.com'
    querystring_auth = False
