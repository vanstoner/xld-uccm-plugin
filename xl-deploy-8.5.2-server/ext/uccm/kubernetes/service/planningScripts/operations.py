import uccm.deltas.compute

reload(uccm.deltas.compute)
from uccm.deltas.compute import DeltasBuilder, StepGenerator


class ServiceStepGenerator(StepGenerator):

    def create(self, delta, deployed, port):
        if port.exposeAsService:
            context.addStepWithCheckpoint(steps.kubectlApply(**{'resource': 'service', 'order': 63, 'ci': port}), delta)
            context.addStep(steps.waitResourceUp(
                **{'resource': 'service', 'resourceName': '{0}-{1}-service'.format(deployed.name, port.name),
                   'ci': port,
                   'order': 64}))

    def destroy(self, delta, deployed, port):
        if port.exposeAsService:
            data = {'target': deployed, 'resource': 'service',
                    'resourceName': '{0}-{1}-service'.format(deployed.name, port.name), 'order': 43}
            context.addStep(steps.noop(**{
                'description': 'Wait for Service {1}/{0} deleted on {2}'.format(port.name, deployed.name,
                                                                                deployed.container.name), 'order': 44}))
            print data
            context.addStepWithCheckpoint(steps.kubectlDelete(**data), delta)


import traceback
import sys

try:
    builder = DeltasBuilder()
    list_of_deltas = builder.build2(delta.operation, deployed, previousDeployed, "ports")
    print "services %s" % list_of_deltas
    ServiceStepGenerator(delta, list_of_deltas).generate()
except:
    # Display the *original* exception
    print(traceback.format_exc())
    sys.exit(1)
