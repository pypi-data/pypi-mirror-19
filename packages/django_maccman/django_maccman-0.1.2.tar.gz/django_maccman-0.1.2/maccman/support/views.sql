-- A view for postfix to find the correct mailboxes
drop view if exists postfix_mailbox cascade;
create view postfix_mailbox as
  select
    concat(maccman_mailbox.account, '@', maccman_domain.name) as address,
    concat(maccman_mailbox.account, '/') as maildir
  from maccman_mailbox
  join maccman_domain on (maccman_mailbox.domain_id = maccman_domain.id)
  where maccman_mailbox.enabled = true and maccman_domain.enabled = true;

-- A view for postfix to find a virtual domain
drop view if exists postfix_domain;
create view postfix_domain as
  select
    name
  from maccman_domain
  where enabled = true;

-- A view for postfix to resolve aliases
drop view if exists postfix_alias;
create view postfix_alias as
  select
    concat(maccman_alias.account, '@', maccman_domain.name) as alias,
    string_agg(maccman_target.address, ', ') as destination
  from maccman_alias
  join maccman_aliases_targets on (maccman_alias.id = maccman_aliases_targets.alias_id)
  join maccman_target on (maccman_target.id = maccman_aliases_targets.target_id)
  join maccman_domain on (maccman_domain.id = maccman_alias.domain_id)
  where maccman_alias.enabled = true and maccman_domain.enabled = true
  group by alias, account;

-- A view for dovecot to find the correct mailboxes
drop view if exists dovecot_user;
create view dovecot_user as
  select
    address as user,
    maildir
  from postfix_mailbox;

-- A view for dovecot to authenticate users
drop view if exists dovecot_password;
create view dovecot_password as
  select
    concat(maccman_mailbox.account, '@', maccman_domain.name) as user,
    maccman_mailbox.password
  from maccman_mailbox
  join maccman_domain on (maccman_mailbox.domain_id = maccman_domain.id)
  where maccman_mailbox.enabled = true and maccman_domain.enabled = true;

-- A view for dovecot to iterate its users
drop view if exists dovecot_iterate;
create view dovecot_iterate as
  select
    concat(maccman_mailbox.account, '@', maccman_domain.name) as user
  from maccman_mailbox
  join maccman_domain on (maccman_mailbox.domain_id = maccman_domain.id)
  where maccman_mailbox.enabled = true and maccman_domain.enabled = true;

