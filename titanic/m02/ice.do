cd "D:\Dropbox\Projects\ml_titanic\data"

insheet using "train.csv", clear case names
save train, replace

insheet using "test.csv", clear case names
gen test=1
append using train

keep PassengerId Pclass Sex Age SibSp Parch Fare Embarked Survived test
encode Sex, gen(nSex)
encode Embarked, gen(nEmbarked)

misschk Pclass nSex Age SibSp Parch Fare Embarked Survived, gen(m)
mi set flong
mi misstable sum 
mi register imputed Pclass nSex Age SibSp Parch Fare nEmbarked Survived 

* ologit is used to take care of the count like distributional properties of these variables. 
mi impute chained (regress) Age Fare (logit) Survived = Pclass nSex SibSp Parch nEmbarked, add(100) rseed(1265852) 

save all_pred, replace

use all_pred, clear
drop if _mi_m == 0
keep if test == 1
keep PassengerId Survived _mi_m
collapse (median) Survived, by(PassengerId)

replace Survived = 1 if Survived == 0.5

export delimited using "ice_results", replace
