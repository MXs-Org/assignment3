## Music Catalog

| Endpoint      | Vulnerability|
| ------------- | -------------|
| http://ec2-52-77-254-209.ap-southeast-1.compute.amazonaws.com:8080/princess.php?target=http://ec2-52-77-254-209.ap-southeast-1.compute.amazonaws.com:8080/adventure/ | Open Redirect |
| http://ec2-52-77-254-209.ap-southeast-1.compute.amazonaws.com:8080/adventure/boogle/googla/peach/?princess=princess.txt | Directory Traversal |

## Neutron Star Collider

| Endpoint      | Vulnerability|
| ------------- | -------------|
| http://ec2-52-77-254-209.ap-southeast-1.compute.amazonaws.com:8081/secretclub.php?page=drinks#/secretclub.php | Open Redirect |
| http://ec2-52-77-254-209.ap-southeast-1.compute.amazonaws.com:8081/secretclub.php?page=entertainment | CSRF |
| http://ec2-52-77-254-209.ap-southeast-1.compute.amazonaws.com:8081/secretclub.php?page=entertainment | Server Side Code Injection |
| http://ec2-52-77-254-209.ap-southeast-1.compute.amazonaws.com:8081/secretclub.php?page=science | Shell Command Injection | 

## The Terminal

| Endpoint      | Vulnerability|
| ------------- | -------------|
| http://ec2-52-77-254-209.ap-southeast-1.compute.amazonaws.com:8082/escape?target=http://ec2-52-77-254-209.ap-southeast-1.compute.amazonaws.com:8083/escaped.html | Open Redirect |
| http://ec2-52-77-254-209.ap-southeast-1.compute.amazonaws.com:8082/file?filename=motd.txt | Directory Traversal |
| http://ec2-52-77-254-209.ap-southeast-1.compute.amazonaws.com:8082/picturise/date | Shell Command Injection |
