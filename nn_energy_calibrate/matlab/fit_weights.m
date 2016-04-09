[data,tags]=get_scores_and_tags( '../helix/pdb_scores.out' );
data = add_separate_unfolded_energies( data, tags, '../helix/rna_helix_stack_elec.wts' ); 
scores_raw = data.scores(:,1);

turner_rules = init_delG_NN();
[ seq_labels, delG_models_NN ] = get_delG_NN_for_tags( tags, turner_rules );

[ tags_NN, delG_NN, delG_NN_err, coeff_matrix ] = get_NN_linear_combinations( 'turner_rule_linear_combinations.txt', tags );

% Consistency check! predicted turner rules with turner_rules vs. what is in linear_combinations file.
delG_NN_pred = coeff_matrix * delG_models_NN;
for i = 1:length( tags_NN); if  ( abs(delG_NN_pred(i) - delG_NN(i)) > 0.1 ) fprintf( 'Problem with %s: pred %f supplied %f!\n', tags_NN{i}, delG_NN_pred(i), delG_NN(i) ); end; end;

%%%%%%%%%%%%%%%%%%%%%%%%%
score_terms_to_fit = setdiff( data.score_labels( 2:end ), {'unfolded','ref'} );
%score_terms_to_fit = setdiff( data.score_labels( 2:end ), {'unfolded','ref','stack_elec_base_base','stack_elec_base_bb'} );
%score_terms_to_fit = {'score','fa_atr','unfolded','intermol'};

do_the_fit( score_terms_to_fit, delG_NN, delG_NN_err, data, tags_NN, coeff_matrix );
