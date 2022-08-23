# extremes_normative_modelling
Multivariate Extreme Value Theory for brain data.
This code is the compagnion to the paper: 'The Extremes of Normative Modelling' 2022.
In this code, we propose a new framework for understanding and modelling neurobiological extreme atypicalities for individual participants. 
We combine the strength of normative models, to make predictions for individual patients, with multivariate extreme value statistics, which allows us to model the outer centiles accurately.

The main python notebooks are:
- nm_single_idp.ipynb to run a single IDP normative model.
- ukb_process_split_tr_te.ipynb to run the normative models on the cluster using the script ukb_run_nm_torque_char.py automatically. 
- MVET_IDP_PCA.ipynb for estimating the multivariate extreme tails for the IDP data of the ukbiobank.
- MVET_behavioural_validation.ipynb for the correlations between the extreme principal components and behaviour.