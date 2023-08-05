

      ## <div>
      ##   <img src="..." />
      ##   <img src="..." />
      ##   <img src="..." />
      ## </div>

      ## <div>
      ##   <img src="..."/>
      ##   <img src="..."/>
      ##   <img src="..."/>
      ## </div>

      ## <div>
      ##   <span>a</span>
      ##   <span>b</span>
      ##   <span>c</span>
      ## </div>

      ## <div>
      ##   <div>a</div>
      ##   <div>b</div>
      ##   <div>c</div>
      ## </div>

      ## <p>
      ##   <b>enabled=[</b>
      ##   {{iff account.enabled 't1' 'f1'}}
      ##   {{iff account.enabled ' ' ' '}}
      ##   {{iff account.enabled 'T2' 'F2'}}
      ##   <div>
      ##     {{#if bling}}
      ##       {{doog}}
      ##     {{else}}
      ##       {{spam}}
      ##     {{/if}}
      ##   </div>
      ##   <b>]</b>
      ## </p>

  ## {{#if account.person}}
  ##   <span
  ##     {{bind-attr title=account.username}}
  ##     class="person"
  ##     >{{account.person.givenname}} {{account.person.surname}}</span>
  ## {{else}}
  ##   <span class="username">{{account.username}}</span>
  ## {{/if}}
