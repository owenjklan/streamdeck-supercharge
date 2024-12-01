### Use JSON output of iostat with jq to get idle CPU
```shell
iostat -c -o JSON | jq '."sysstat"."hosts"[0]."statistics"[0]."avg-cpu"."idle"'
```