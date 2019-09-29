from ipykernel.kernelbase import Kernel
from assembler.virtual_machine import RISCVMachine
from assembler.assemble import assemble


class RiscvKernel(Kernel):
    implementation = 'riscv_kernel'
    implementation_version = '1.0'
    language = 'riscv'
    language_version = '1.0'
    language_info = {
        'name': 'riscv',
        'mimetype': 'riscv',
        'file_extension': 'x86',
    }
    banner = "Riscv kernel - run riscv assembly language"
    vm_machine = None

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):

        if not silent:
            if not self.vm_machine:
                self.vm_machine = RISCVMachine()
                self.vm_machine.base = 'hex'
                self.vm_machine.flavor = 'riscv'
            (last_instr, error, bit_code) = assemble(code, self.vm_machine)

            if error == "":
                vm_machine_info = {'name': 'riscv_machine_info'}
                vm_machine_info['text'] = str(self.vm_machine.registers)
                self.send_response(self.iopub_socket,
                                   'stream', vm_machine_info)
            else:
                error_msg = {'name': 'error_msg', 'text': error}
                self.send_response(self.iopub_socket, 'stream', error_msg)

        return {'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {}
                }
