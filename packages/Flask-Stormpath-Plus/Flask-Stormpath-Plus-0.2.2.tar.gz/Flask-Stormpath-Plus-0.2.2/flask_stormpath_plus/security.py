
import  hmac, hashlib

def get_secure_val(s, salt):
    '''
    get a hashed password

    :param s: original password
    :param salt: the salt, use the app secret key defautly
    :return:  the hashed password
    '''

    h = hmac.new(salt, s, hashlib.sha256).hexdigest()

    # stormpath need at least one Upper letter and one lOWER
    return  h+'|MitUPPERlower'
