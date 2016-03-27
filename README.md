# Course-Based-Recommendation-System
Course Based Recommendation System to recommend courses based on students preference

### recommender system 
```
https://en.wikipedia.org/wiki/Recommender_system
```

### vagrant, docker, ...

* problem
```
$ vagrant up
WARNING: The character device /dev/vboxdrv does not exist. Please install the virtualbox-dkms package and the appropriate headers, most likely linux-headers-generic. You will not be able to start VMs until this problem is fixed.
```

* solution - https://goo.gl/X0I9fR
```
$ sudo dpkg-reconfigure virtualbox-dkms
$ sudo dpkg-reconfigure virtualbox  
$ vagrant up
```


