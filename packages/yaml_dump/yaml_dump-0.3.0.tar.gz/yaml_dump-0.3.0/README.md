# yaml dump

* Unicode as utf8
* Keep order of OrderedDict

# INSTALL

    pip install yaml_dump 

# USAGE

    from yaml_dump import yaml_dump
    print(yaml_dump(dict(a=1,b=[1,2,3],c="한글")))

# EXAMPLE OUTPUT

    a: 1
    b:
    - 1
    - 2
    - 3
    c: 한글

