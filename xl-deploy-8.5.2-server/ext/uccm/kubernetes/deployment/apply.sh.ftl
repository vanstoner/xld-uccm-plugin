echo '
<#include profile>
' > deployment.json
cat -n deployment.json
kubectl apply -f deployment.json --validate=true -n ${deployed.container.name}


