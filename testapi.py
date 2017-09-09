from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
import Hamlib
import sys

sys.path.append ('.')
sys.path.append ('.libs')


app = Flask(__name__)
api = Api(app)

class Dummy_Test(Resource):
    def get(self):

        Hamlib.rig_set_debug (Hamlib.RIG_DEBUG_NONE)

        # Init RIG_MODEL_DUMMY
        my_rig = Hamlib.Rig (Hamlib.RIG_MODEL_DUMMY)
        my_rig.set_conf ("rig_pathname","/dev/Rig")
        my_rig.set_conf ("retry","5")

        my_rig.open ()

        # 1073741944 is token value for "itu_region"
        # but using get_conf is much more convenient
        region = my_rig.get_conf(1073741944)
        rpath = my_rig.get_conf("rig_pathname")
        retry = my_rig.get_conf("retry")
        print "status(str):\t\t",Hamlib.rigerror(my_rig.error_status)
        print "get_conf:\t\tpath = %s, retry = %s, ITU region = %s" \
            % (rpath, retry, region)

        my_rig.set_freq (Hamlib.RIG_VFO_B, 5700000000)
        my_rig.set_vfo (Hamlib.RIG_VFO_B)
        test = "freq:\t\t\t",my_rig.get_freq()
        my_rig.set_freq (Hamlib.RIG_VFO_A, 145550000)
        #my_rig.set_vfo ("VFOA")

        (mode, width) = my_rig.get_mode()
        print "mode:\t\t\t",Hamlib.rig_strrmode(mode),"\nbandwidth:\t\t",width
        my_rig.set_mode(Hamlib.RIG_MODE_CW)
        (mode, width) = my_rig.get_mode()
        print "mode:\t\t\t",Hamlib.rig_strrmode(mode),"\nbandwidth:\t\t",width

        print "ITU_region:\t\t",my_rig.state.itu_region
        print "Backend copyright:\t",my_rig.caps.copyright

        print "Model:\t\t\t",my_rig.caps.model_name
        print "Manufacturer:\t\t",my_rig.caps.mfg_name
        print "Backend version:\t",my_rig.caps.version
        print "Backend license:\t",my_rig.caps.copyright
        print "Rig info:\t\t", my_rig.get_info()

        my_rig.set_level ("VOX",  1)
        print "VOX level:\t\t",my_rig.get_level_i("VOX")
        my_rig.set_level (Hamlib.RIG_LEVEL_VOX, 5)
        print "VOX level:\t\t", my_rig.get_level_i(Hamlib.RIG_LEVEL_VOX)

        print "strength:\t\t", my_rig.get_level_i(Hamlib.RIG_LEVEL_STRENGTH)
        print "status:\t\t\t",my_rig.error_status
        print "status(str):\t\t",Hamlib.rigerror(my_rig.error_status)

        chan = Hamlib.channel(Hamlib.RIG_VFO_B)

        my_rig.get_channel(chan)
        print "get_channel status:\t",my_rig.error_status

        print "VFO:\t\t\t",Hamlib.rig_strvfo(chan.vfo),", ",chan.freq

        print "\nSending Morse, '73'"
        my_rig.send_morse(Hamlib.RIG_VFO_A, "73")

        my_rig.close ()

        return


api.add_resource(Dummy_Test, '/test')

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=80)
