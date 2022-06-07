
import delimited "/Users/juantrujillo/Desktop/HE1/EntregaFinal-HE1/ML_df.csv"

encode position, gen(pos_categ)
encode team, gen(team_categ)

drop position
drop team
drop group_min
drop name 

asdoc reg min_norm fld_sd off_sd crs_sd tklw_sd int_sd og_sd min_n gls_n ast_n pk_n pkatt_n crdy_n crdr_n sh_n sot_n fls_n fld_n off_n crs_n int_n tklw_n og_n competition pos_categ team_categ

