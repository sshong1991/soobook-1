FROM        hm07/soobook
MAINTAINER  gusals3407@gmail.com


WORKDIR     /srv/app/django_app
EXPOSE      4567
CMD ["supervisord", "-n"]