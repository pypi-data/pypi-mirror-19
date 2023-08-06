import shutit_standalone
import logging
shutit_obj = shutit_standalone.create_bash_session()
username = shutit_obj.get_input('Input username: ')
password = shutit_obj.get_input('Input password', ispass=True)
shutit_obj.login('ssh ' + username + '@shutit.tk',
                 password=password)
shutit_obj.install('git') #isinstalled?
shutit_obj.logout()
