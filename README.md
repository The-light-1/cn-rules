# GL.iNet CN Direct Builder

This repository builds `cn-direct.txt` from the current MetaCubeX lists:

- `geo/geosite/cn.list`
- `geo/geoip/cn.list`

The builder converts `+.example.com` into `example.com`, filters unsupported lines,
keeps valid IPv4 / IPv4 CIDR entries, removes duplicates, and writes UTF-8 plain text.

## Use

1. Put these files in a GitHub repository.
2. Open **Actions** and run **Update CN direct list** once.
3. After `cn-direct.txt` appears, use its GitHub **Raw** URL in GL.iNet:

   VPN Dashboard → edit tunnel → Target Destination →
   Exclude Specified Domain / IP List → Subscription URL

Example Raw URL:

`https://raw.githubusercontent.com/YOUR_NAME/YOUR_REPO/main/cn-direct.txt`

The workflow also refreshes the file once per day.
