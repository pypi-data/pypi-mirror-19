

(function(globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    var v=(n%10!=1 || n%100==11);
    if (typeof(v) == 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  var newcatalog = {
    "#%(position)s": "#%(position)s", 
    "%(count)s language matches your query.": [
      "%(count)s tungum\u00e1l samsvarar fyrirspurn \u00feinni.", 
      "%(count)s tungum\u00e1l samsvara fyrirspurn \u00feinni."
    ], 
    "%(count)s project matches your query.": [
      "%(count)s verkefni samsvarar fyrirspurn \u00feinni.", 
      "%(count)s verkefni samsvara fyrirspurn \u00feinni."
    ], 
    "%(count)s user matches your query.": [
      "%(count)s notandi samsvarar fyrirspurn \u00feinni.", 
      "%(count)s notendur samsvara fyrirspurn \u00feinni."
    ], 
    "%(timeSince)s via file upload": "%(timeSince)s me\u00f0 innsendri skr\u00e1", 
    "%s hour": [
      "%s klukkustund", 
      "%s klukkustundir"
    ], 
    "%s word": [
      "%s or\u00f0", 
      "%s or\u00f0"
    ], 
    "%s's accepted suggestions": "%s vi\u00f0urkenndar upp\u00e1stungur", 
    "%s's overwritten submissions": "%s yfirskrifa\u00f0ar upp\u00e1stungur", 
    "%s's pending suggestions": "%s \u00f3kl\u00e1ra\u00f0ar upp\u00e1stungur", 
    "%s's rejected suggestions": "%s upp\u00e1stungum sem hefur veri\u00f0 hafna\u00f0", 
    "%s's submissions": "%s upp\u00e1stungur", 
    "(registered tasks)": "(skr\u00e1\u00f0 verk)", 
    "+%(score)s": "+%(score)s", 
    "Accept": "Sam\u00feykkja", 
    "Account Activation": "Virkjun a\u00f0gangs", 
    "Account Inactive": "A\u00f0gangur er \u00f3virkur", 
    "Action": "A\u00f0ger\u00f0", 
    "Active": "Virkt", 
    "Add Language": "B\u00e6ta vi\u00f0 tungum\u00e1li", 
    "Add Project": "B\u00e6ta vi\u00f0 verkefni", 
    "Add User": "B\u00e6ta vi\u00f0 notanda", 
    "Administrator": "Kerfisstj\u00f3ri", 
    "All Languages": "\u00d6ll tungum\u00e1l", 
    "All Projects": "\u00d6ll verkefni", 
    "Amount": "Magn", 
    "An error occurred while attempting to sign in via %s.": "\u00d3v\u00e6nt villa kom upp \u00feegar reynt var a\u00f0 skr\u00e1 inn me\u00f0 %s.", 
    "Avatar": "Au\u00f0kennismynd", 
    "Cancel": "H\u00e6tta vi\u00f0", 
    "Clear all": "Hreinsa allt", 
    "Clear value": "Hreinsa gildi", 
    "Close": "Loka", 
    "Code": "K\u00f3\u00f0i", 
    "Collapse details": "Loka sm\u00e1atri\u00f0um", 
    "Comment": "Athugasemd", 
    "Comment on it": "Ger\u00f0u athugasemd vi\u00f0 \u00fea\u00f0", 
    "Congratulations! You have completed this task!": "Til hamingju, \u00fe\u00fa hefur loki\u00f0 \u00feessu verki!", 
    "Contact Us": "Haf\u00f0u samband vi\u00f0 okkur", 
    "Contributors, 30 Days": "\u00de\u00e1tttakendur, 30 dagar", 
    "Datetime": "DagsetningT\u00edmi", 
    "Delete": "Ey\u00f0a", 
    "Deleted successfully.": "T\u00f3kst a\u00f0 ey\u00f0a.", 
    "Disabled": "\u00d3virkt", 
    "Discard changes.": "Henda breytingum.", 
    "Edit Language": "Breyta tungum\u00e1li", 
    "Edit My Public Profile": "Breyta opinberri notandas\u00ed\u00f0u minni", 
    "Edit Project": "Breyta verkefni", 
    "Edit User": "Breyta notanda", 
    "Email": "T\u00f6lvup\u00f3stfang", 
    "Email Address": "T\u00f6lvup\u00f3stfang", 
    "Email Confirmation": "Sta\u00f0festing \u00ed t\u00f6lvup\u00f3sti", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "Sl\u00e1\u00f0u inn netfangi\u00f0 sem \u00fe\u00fa skr\u00e1\u00f0ir \u00feig me\u00f0, vi\u00f0 munum senda tengil \u00e1 \u00fea\u00f0 sem \u00fe\u00fa getur nota\u00f0 til a\u00f0 breyta lykilor\u00f0inu \u00fe\u00ednu.", 
    "Entire Project": "Allt verkefni\u00f0", 
    "Error while connecting to the server": "Villa vi\u00f0 a\u00f0 tengjast \u00fej\u00f3ni", 
    "Expand details": "Birta sm\u00e1atri\u00f0i", 
    "File types": "Skr\u00e1ategundir", 
    "Filesystems": "Skr\u00e1akerfi", 
    "Find language by name, code": "Finna tungum\u00e1l eftir nafni, k\u00f3\u00f0a", 
    "Find project by name, code": "Finna verkefni eftir nafni, k\u00f3\u00f0a", 
    "Find user by name, email, properties": "Finndu notanda eftir nafni, t\u00f6lvup\u00f3stfangi, eiginleikum", 
    "Full Name": "Fullt nafn", 
    "Go back to browsing": "Fara aftur \u00ed vafur", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "Fara \u00e1 n\u00e6sta streng (Ctrl+.)<br/><br/>Einnig:<br/>N\u00e6sta s\u00ed\u00f0a: Ctrl+Shift+.<br/>S\u00ed\u00f0asta s\u00ed\u00f0a: Ctrl+Shift+End", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "Fara \u00e1 fyrri streng (Ctrl+,)<br/><br/>Einnig:<br/>Fyrri s\u00ed\u00f0a: Ctrl+Shift+,<br/>Fyrsta s\u00ed\u00f0a: Ctrl+Shift+Home", 
    "Hide": "Fela", 
    "Hide disabled": "Fela \u00f3virkt", 
    "I forgot my password": "\u00c9g gleymdi lykilor\u00f0inu m\u00ednu", 
    "Ignore Files": "Hunsa skr\u00e1r", 
    "Languages": "Tungum\u00e1l", 
    "Less": "Minna", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "Sl\u00f3\u00f0 \u00e1 LinkedIn notandasni\u00f0", 
    "Load More": "Hla\u00f0a inn meiru", 
    "Loading...": "Hle\u00f0 inn...", 
    "Login / Password": "Innskr\u00e1ning / Lykilor\u00f0", 
    "More": "Meira", 
    "More...": "Meira...", 
    "My Public Profile": "Opinber notandas\u00ed\u00f0a m\u00edn", 
    "No": "Nei", 
    "No activity recorded in a given period": "Engin virkni skr\u00e1\u00f0 \u00e1 uppgefnu t\u00edmabili", 
    "No results found": "Engar ni\u00f0urst\u00f6\u00f0ur fundust", 
    "No results.": "Engar ni\u00f0urst\u00f6\u00f0ur.", 
    "No, thanks": "Nei, takk", 
    "Not found": "Fannst ekki", 
    "Number of Plurals": "Fleirt\u00f6lur", 
    "Oops...": "\u00dabbs...", 
    "Overview": "Yfirlit", 
    "Password": "Lykilor\u00f0", 
    "Password changed, signing in...": "Lykilor\u00f0i breytt, skr\u00e1i inn...", 
    "Period": "T\u00edmabil", 
    "Permissions": "Heimildir", 
    "Personal description": "Pers\u00f3nul\u00fdsing", 
    "Personal website URL": "Sl\u00f3\u00f0 \u00e1 eigi\u00f0 vefsv\u00e6\u00f0i", 
    "Please select a valid user.": "Veldu einhvern gildan notanda.", 
    "Plural Equation": "Fleirt\u00f6lujafna", 
    "Plural form %(index)s": "Fleirt\u00f6luform %(index)s", 
    "Preview will be displayed here.": "Forsko\u00f0un mun birtast h\u00e9r.", 
    "Project / Language": "Verkefni / Tungum\u00e1l", 
    "Project Tree Style": "Greinast\u00edll verkefnis", 
    "Public Profile": "Opinberar uppl\u00fdsingar", 
    "Quality Checks": "G\u00e6\u00f0apr\u00f3fanir", 
    "Rate": "Stig", 
    "Registered Tasks": "Skr\u00e1\u00f0 verk", 
    "Reject": "Hafna", 
    "Reload page": "Endurlesa s\u00ed\u00f0u", 
    "Remove task": "Fjarl\u00e6gja verk", 
    "Repeat Password": "Endurtaka lykilor\u00f0", 
    "Resend Email": "Endursenda t\u00f6lvup\u00f3st", 
    "Reset Password": "Endurstilla lykilor\u00f0", 
    "Reset Your Password": "Endurstilltu lykilor\u00f0i\u00f0 \u00feitt", 
    "Reviewed": "Yfirfari\u00f0", 
    "Save": "Vista", 
    "Saved successfully.": "T\u00f3kst a\u00f0 vista.", 
    "Score Change": "Breyting \u00e1 skori", 
    "Search Languages": "Leita a\u00f0 tungum\u00e1li", 
    "Search Projects": "Leita a\u00f0 verkefni", 
    "Search Users": "Leita a\u00f0 notendum", 
    "Select...": "Velja...", 
    "Send Email": "Senda t\u00f6lvup\u00f3st", 
    "Sending email to %s...": "Sendi t\u00f6lvup\u00f3st til %s...", 
    "Server error": "Villa fr\u00e1 \u00fej\u00f3ni", 
    "Set New Password": "Stilla n\u00fdtt lykilor\u00f0", 
    "Set a new password": "Stilla n\u00fdtt lykilor\u00f0", 
    "Settings": "Stillingar", 
    "Short Bio": "Stutt \u00e6vi\u00e1grip", 
    "Show": "S\u00fdna", 
    "Show disabled": "Birta \u00f3virkt", 
    "Sign In": "Skr\u00e1 inn", 
    "Sign In With %s": "Skr\u00e1 inn me\u00f0 %s", 
    "Sign In With...": "Skr\u00e1 inn me\u00f0...", 
    "Sign Up": "Skr\u00e1 sig", 
    "Sign in as an existing user": "Skr\u00e1 inn sem \u00feegar skr\u00e1\u00f0ur notandi", 
    "Sign up as a new user": "Skr\u00e1 inn sem n\u00fdr notandi", 
    "Signed in. Redirecting...": "Skr\u00e1\u00f0ur inn. Endurbeini...", 
    "Similar translations": "Svipa\u00f0ar \u00fe\u00fd\u00f0ingar", 
    "Source Language": "Upprunatungum\u00e1l", 
    "Special Characters": "S\u00e9rt\u00e1kn", 
    "String Errors Contact": "Tengili\u00f0ur vegna villna \u00ed textastrengjum", 
    "Subtotal": "Millisamtala", 
    "Suggested": "Stungi\u00f0 upp\u00e1", 
    "Summary": "Samantekt", 
    "Team": "Teymi", 
    "The server seems down. Try again later.": "\u00dej\u00f3nninn vir\u00f0ist vera ni\u00f0ri. Vinsamlega reyndu s\u00ed\u00f0ar.", 
    "There are unsaved changes. Do you want to discard them?": "\u00dea\u00f0 eru \u00f3vista\u00f0ar breytingar. Viltu henda \u00feeim?", 
    "There is %(count)s language.": [
      "\u00dea\u00f0 er %(count)s tungum\u00e1l.", 
      "\u00dea\u00f0 eru %(count)s tungum\u00e1l."
    ], 
    "There is %(count)s project.": [
      "\u00dea\u00f0 er %(count)s verkefni.", 
      "\u00dea\u00f0 eru %(count)s verkefni."
    ], 
    "There is %(count)s user.": [
      "\u00dea\u00f0 er %(count)s notandi.", 
      "\u00dea\u00f0 eru %(count)s notendur. Fyrir ne\u00f0an eru \u00feeir sem s\u00ed\u00f0ast var b\u00e6tt vi\u00f0."
    ], 
    "Total (%(currency)s)": "Samtals (%(currency)s)", 
    "Translated": "B\u00fai\u00f0 a\u00f0 \u00fe\u00fd\u00f0a", 
    "Translated by %(fullname)s in &ldquo;<span title=\"%(path)s\">%(project)s</span>&rdquo; project": "\u00de\u00fdtt af %(fullname)s \u00ed &ldquo;<span title=\"%(path)s\">%(project)s</span>&rdquo; verkefninu", 
    "Translated by %(fullname)s in &ldquo;<span title=\"%(path)s\">%(project)s</span>&rdquo; project %(time_ago)s": "\u00de\u00fdtt af %(fullname)s \u00ed &ldquo;<span title=\"%(path)s\">%(project)s</span>&rdquo; verkefninu fyrir %(time_ago)s s\u00ed\u00f0an", 
    "Try again": "Reyndu aftur", 
    "Twitter": "Twitter", 
    "Twitter username": "Twitter notandanafn", 
    "Type to search": "Skrifa\u00f0u til a\u00f0 leita...", 
    "Updating data": "Uppf\u00e6ri g\u00f6gn", 
    "Username": "Notandanafn", 
    "Website": "Vefsv\u00e6\u00f0i", 
    "Yes": "J\u00e1", 
    "Your Full Name": "Fullt nafn \u00feitt", 
    "Your LinkedIn profile URL": "LinkedIn notandasni\u00f0i\u00f0 mitt", 
    "Your Personal website/blog URL": "Sl\u00f3\u00f0 \u00e1 \u00feitt eigi\u00f0 vefsv\u00e6\u00f0i/blogg", 
    "Your Twitter username": "Twitter notandanafni\u00f0 \u00feitt", 
    "Your account needs activation.": "Virkja \u00fearf a\u00f0ganginn \u00feinn.", 
    "disabled": "\u00f3virkt", 
    "some anonymous user": "einhver nafnlaus notandi", 
    "someone": "einhver"
  };
  for (var key in newcatalog) {
    django.catalog[key] = newcatalog[key];
  }
  

  if (!django.jsi18n_initialized) {
    django.gettext = function(msgid) {
      var value = django.catalog[msgid];
      if (typeof(value) == 'undefined') {
        return msgid;
      } else {
        return (typeof(value) == 'string') ? value : value[0];
      }
    };

    django.ngettext = function(singular, plural, count) {
      var value = django.catalog[singular];
      if (typeof(value) == 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value[django.pluralidx(count)];
      }
    };

    django.gettext_noop = function(msgid) { return msgid; };

    django.pgettext = function(context, msgid) {
      var value = django.gettext(context + '\x04' + msgid);
      if (value.indexOf('\x04') != -1) {
        value = msgid;
      }
      return value;
    };

    django.npgettext = function(context, singular, plural, count) {
      var value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.indexOf('\x04') != -1) {
        value = django.ngettext(singular, plural, count);
      }
      return value;
    };

    django.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    django.formats = {
    "DATETIME_FORMAT": "N j, Y, P", 
    "DATETIME_INPUT_FORMATS": [
      "%Y-%m-%d %H:%M:%S", 
      "%Y-%m-%d %H:%M:%S.%f", 
      "%Y-%m-%d %H:%M", 
      "%Y-%m-%d", 
      "%m/%d/%Y %H:%M:%S", 
      "%m/%d/%Y %H:%M:%S.%f", 
      "%m/%d/%Y %H:%M", 
      "%m/%d/%Y", 
      "%m/%d/%y %H:%M:%S", 
      "%m/%d/%y %H:%M:%S.%f", 
      "%m/%d/%y %H:%M", 
      "%m/%d/%y"
    ], 
    "DATE_FORMAT": "N j, Y", 
    "DATE_INPUT_FORMATS": [
      "%Y-%m-%d", 
      "%m/%d/%Y", 
      "%m/%d/%y", 
      "%b %d %Y", 
      "%b %d, %Y", 
      "%d %b %Y", 
      "%d %b, %Y", 
      "%B %d %Y", 
      "%B %d, %Y", 
      "%d %B %Y", 
      "%d %B, %Y"
    ], 
    "DECIMAL_SEPARATOR": ".", 
    "FIRST_DAY_OF_WEEK": "0", 
    "MONTH_DAY_FORMAT": "F j", 
    "NUMBER_GROUPING": "0", 
    "SHORT_DATETIME_FORMAT": "m/d/Y P", 
    "SHORT_DATE_FORMAT": "m/d/Y", 
    "THOUSAND_SEPARATOR": ",", 
    "TIME_FORMAT": "P", 
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S", 
      "%H:%M:%S.%f", 
      "%H:%M"
    ], 
    "YEAR_MONTH_FORMAT": "F Y"
  };

    django.get_format = function(format_type) {
      var value = django.formats[format_type];
      if (typeof(value) == 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = django.pluralidx;
    globals.gettext = django.gettext;
    globals.ngettext = django.ngettext;
    globals.gettext_noop = django.gettext_noop;
    globals.pgettext = django.pgettext;
    globals.npgettext = django.npgettext;
    globals.interpolate = django.interpolate;
    globals.get_format = django.get_format;

    django.jsi18n_initialized = true;
  }

}(this));

