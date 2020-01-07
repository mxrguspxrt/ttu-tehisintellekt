mees('Marcus').
mees('Jaan').
mees('Ivan').

riigi_elanik('Marcus', 'Pompej').
riigi_elanik('Francesco', 'Pompej').

syndis('Marcus', 1940).
syndis('Jaan', 1977).
syndis('Francesco', 1989).

katastroof('Pompej', 1970).

kuupaev('T2na', 2019).



surelik(Nimi) :-
    mees(Nimi).

katastroofi_ohver(Nimi) :- 
    riigi_elanik(Nimi, Riik), 
    katastroof(Riik, KatastroofiAasta),
    syndis(Nimi, SynniAasta), 
    SynniAasta < KatastroofiAasta. 

vanadusse_surnud(Nimi) :-
    surelik(Nimi),
    syndis(Nimi, SynniAasta),
    kuupaev('T2na', T2naneAasta),
    SynniAasta + 150 < T2naneAasta.
    
surnud(Nimi) :- 
    katastroofi_ohver(Nimi) ; vanadusse_surnud(Nimi).



% surnud('Marcus').
% surnud('Jaan').
% surnud('Francesco').
% surnud('Ivan').
% commencement(Date):- Date >= 1982.
