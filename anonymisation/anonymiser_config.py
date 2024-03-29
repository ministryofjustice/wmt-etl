'''
Application configuration settings
'''
# Extract file settings
IMPORT_FILE_DIR = ('./input_files')
EXPECTED_FILE_EXTENSIONS = ('.xlsx', '.xls')

# Extract valid source worksheet tabs
VALID_SHEET_NAMES = [
    'wmt_extract',
    'wmt_extract_filtered',
    'court_reports',
    'inst_reports',
    'flag_warr_4_n',
    'flag_upw',
    'flag_o_due',
    'flag_priority',
    'cms',
    'gs',
    'arms',
    't2a',
    'wmt_extract_sa',
    'suspended_lifers',
    't2a_detail',
    'omic_teams']

VALID_COLUMNS = {'wmt_extract': ['trust','region_desc','region_code','ldu_desc','ldu_code','team_desc','team_code','om_surname','om_forename','om_grade_code','om_key','custtier0','commtier0','licencetier0','commtierd0','commtierd1','commtierd2','commtierd3','commtierc0','commtierc1','commtierc2','commtierc3','commtierb0','commtierb1','commtierb2','commtierb3','commtiera0','commtiera1','commtiera2','commtiera3','licencetierd0','licencetierd1','licencetierd2','licencetierd3','licencetierc0','licencetierc1','licencetierc2','licencetierc3','licencetierb0','licencetierb1','licencetierb2','licencetierb3','licencetiera0','licencetiera1','licencetiera2','licencetiera3','custtierd0','custtierd1','custtierd2','custtierd3','custtierc0','custtierc1','custtierc2','custtierc3','custtierb0','custtierb1','custtierb2','custtierb3','custtiera0','custtiera1','custtiera2','custtiera3','comin1st16weeks','licin1st16weeks','datestamp','vcrn_count','pdu_code','pdu_desc'],
    'wmt_extract_filtered': ['trust','region_desc','region_code','ldu_desc','ldu_code','team_desc','team_code','om_surname','om_forename','om_grade_code','om_key','custtier0','commtier0','licencetier0','commtierd0','commtierd1','commtierd2','commtierd3','commtierc0','commtierc1','commtierc2','commtierc3','commtierb0','commtierb1','commtierb2','commtierb3','commtiera0','commtiera1','commtiera2','commtiera3','licencetierd0','licencetierd1','licencetierd2','licencetierd3','licencetierc0','licencetierc1','licencetierc2','licencetierc3','licencetierb0','licencetierb1','licencetierb2','licencetierb3','licencetiera0','licencetiera1','licencetiera2','licencetiera3','custtierd0','custtierd1','custtierd2','custtierd3','custtierc0','custtierc1','custtierc2','custtierc3','custtierb0','custtierb1','custtierb2','custtierb3','custtiera0','custtiera1','custtiera2','custtiera3','comin1st16weeks','licin1st16weeks','datestamp','vcrn_count','pdu_code','pdu_desc'],
    'court_reports': ['team_desc','team_code','om_key','om_team_staff_grade','sdr_last_30','sdr_due_next_30','sdr_conv_last_30','datestamp','oral_reports','trust','region_desc','region_code','ldu_desc','ldu_code','om_surname','om_forename','om_grade_code','pdu_code','pdu_desc'],
    'inst_reports': ['team_desc','team_code','om_name','om_key','om_team_staff_grade','parom_due_next_30','parom_comp_last_30','datestamp'],
    'flag_warr_4_n': ['row_type','case_ref_no','tier_code','team_code','om_grade_code','om_key','location'],
    'flag_upw': ['row_type','case_ref_no','tier_code','team_code','om_grade_code','om_key','location'],
    'flag_o_due': ['row_type','case_ref_no','tier_code','team_code','om_grade_code','om_key','location'],
    'flag_priority': ['row_type','case_ref_no','tier_code','team_code','om_grade_code','om_key','location'],
    'cms': ['contact_id','contact_date','contact_type_code','contact_type_desc','contact_staff_name','contact_staff_key','contact_staff_grade','contact_team_key','contact_provider_code','om_name','om_key','om_grade','om_team_key','om_provider_code','crn'],
    'gs': ['contact_id','contact_date','contact_type_code','contact_type_desc','om_name','om_key','om_grade','om_team_key','om_provider_code','crn'],
    'arms': ['assessment_date','assessment_code','assessment_desc','assessment_staff_name','assessment_staff_key','assessment_staff_grade','assessment_team_key','assessment_provider_code','crn','disposal_or_release_date','sentence_type','so_registration_date','asmnt_outcome_cd','asmnt_outcome_desc','last_saved_dt_referral_doc','last_saved_dt_assessment_doc','offender_manager_staff_name','offender_manager_team_cd','offender_manager_cluster_cd','offender_manager_provider_cd','completed_date','offender_manager_pdu_cd'],
    't2a': ['trust','region_desc','region_code','ldu_desc','ldu_code','team_desc','team_code','om_surname','om_forename','om_grade_code','om_key','custtier0','commtier0','licencetier0','commtierd0','commtierd1','commtierd2','commtierd3','commtierc0','commtierc1','commtierc2','commtierc3','commtierb0','commtierb1','commtierb2','commtierb3','commtiera0','commtiera1','commtiera2','commtiera3','licencetierd0','licencetierd1','licencetierd2','licencetierd3','licencetierc0','licencetierc1','licencetierc2','licencetierc3','licencetierb0','licencetierb1','licencetierb2','licencetierb3','licencetiera0','licencetiera1','licencetiera2','licencetiera3','custtierd0','custtierd1','custtierd2','custtierd3','custtierc0','custtierc1','custtierc2','custtierc3','custtierb0','custtierb1','custtierb2','custtierb3','custtiera0','custtiera1','custtiera2','custtiera3','comin1st16weeks','licin1st16weeks','datestamp','vcrn_count','pdu_code','pdu_desc'],
    'wmt_extract_sa': ['case_ref_no','tier_code','team_code','om_grade_code','om_key','location','disposal_type_desc','disposal_type_code','standalone_order','row_type'],
    'suspended_lifers': ['location','row_type','case_ref_no','tier_code','team_code','om_grade_code','om_key','in_custody','register_code','register_description','register_level','register_level_description','register_category','register_category_description','registration_date','next_review_date','deregistration_date'],
    't2a_detail': ['crn','event_no','allocation_date','allocation_reason','allocation_cd','provider_code_order_manager','cluster_order_manager','cluster_cd_order_manager','team_order_manager','team_cd_order_manager','staff_name_order_manager','staff_cd_order_manager','nsi_cd','nsi_desc','birth_date','age','nsi_status_cd','nsi_status_desc','nsi_outcome_cd','nsi_outcome_desc','staff_name_offender_manager','staff_cd_offender_manager','staff_grade_cd_offender_manager','provider_cd_offender_manager','cluster_cd_offender_manager','team_cd_offender_manager','pdu_order_manager','pdu_cd_order_manager','allocation_desc','pdu_cd_offender_manager'],
    'omic_teams': ['trust','region_desc','region_code','ldu_desc','ldu_code','team_desc','team_code','om_surname','om_forename','om_grade_code','om_key','custtier0','commtier0','licencetier0','commtierd0','commtierd1','commtierd2','commtierd3','commtierc0','commtierc1','commtierc2','commtierc3','commtierb0','commtierb1','commtierb2','commtierb3','commtiera0','commtiera1','commtiera2','commtiera3','licencetierd0','licencetierd1','licencetierd2','licencetierd3','licencetierc0','licencetierc1','licencetierc2','licencetierc3','licencetierb0','licencetierb1','licencetierb2','licencetierb3','licencetiera0','licencetiera1','licencetiera2','licencetiera3','custtierd0','custtierd1','custtierd2','custtierd3','custtierc0','custtierc1','custtierc2','custtierc3','custtierb0','custtierb1','custtierb2','custtierb3','custtiera0','custtiera1','custtiera2','custtiera3','comin1st16weeks','licin1st16weeks','datestamp','vcrn_count','pdu_code','pdu_desc']}
