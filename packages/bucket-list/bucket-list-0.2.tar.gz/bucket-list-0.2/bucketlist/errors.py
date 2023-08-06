class BucketlistError(Exception):
    def __init__(self, description):
        Exception.__init__(self)
        self.description = description

    def jsonify(self):
        return {
            'description': self.description
        }

    def __str__(self):
        return "{}".format(self.description)
