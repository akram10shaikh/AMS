from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from player_app import views

urlpatterns = [
                  path('', views.player_list, name='player_list'),
                  path('player/<int:pk>/', views.player_detail, name='player_detail'),
                  path('player/new/', views.player_create, name='player_create'),
                  path('player/<int:pk>/edit/', views.player_update, name='player_update'),
                  path('player/<int:pk>/home/', views.player_home, name='player_home'),
                  path('player/<int:pk>/delete/', views.player_delete, name='player_delete'),
                  path("upload/", views.upload_file, name="upload_file"),
                  path('download-blank-excel/', views.download_blank_excel, name='download_blank_excel'),
                  path('players/export/', views.export_players_to_excel, name='export_players_to_excel'),

                  path('player/<int:player_id>/upload_medical_documents/', views.upload_medical_documents, name='upload_medical_documents'),

                  path('groups/', views.manage_all_groups, name='manage_all_groups'),
                  path('get_all_players/', views.get_all_players, name='get_all_players'),

                  path('groups/manage/', views.manage_groups, name='manage_groups'),
                  path('get_group_players/', views.get_all_group_players, name='get_group_players'),
                  path('rename_group/', views.rename_group, name='rename_group'),
                  path('delete_group/<int:group_id>/', views.delete_group, name='delete_group'),

                  path('camps_tournaments/', views.camps_tournaments, name='camps_tournaments'),
                  path('camp/<int:camp_id>/', views.camp_detail, name='camp_detail'),  # Add this
                  path('camp/create/', views.create_camp, name='create_camp'),
                  path('camp/<int:camp_id>/edit/', views.edit_camp, name='edit_camp'),
                  path('camp/<int:camp_id>/delete/', views.delete_camp, name='delete_camp'),

                  path('trash_camps/', views.trash_camps, name='trash_camps'),
                  path('trash_camps/restore/<int:camp_id>/', views.restore_camp, name='restore_camp'),
                  path('trash_camps/delete/<int:camp_id>/', views.permanently_delete_camp, name='permanently_delete_camp'),

                  path('camp/<int:camp_id>/activity/download/', views.download_activity_history,
                       name='download_activity_history'),

                  path('programs/create/', views.create_program, name='create_program'),
                  path('programs/assign/', views.assign_program, name='assign_program'),
                  path('programs/<int:program_id>/save_workout/', views.save_workout_data, name='save_workout_data'),
                  path('programs/list/', views.program_list, name='program_list'),

                  # path('player/home/', views.player_home, name='player_home'),
                  
                  path('injury/create/', views.create_injury, name='create_injury'),
                  path('injuries/', views.injury_list, name='injury_list'),
                  path('injury/update/<int:pk>/', views.update_injury, name='update_injury'),
                  path('injury/update-status/<int:pk>/', views.update_injury_status, name='update_injury_status'),
                  path('injuries/confirm-close/<int:pk>/', views.confirm_close, name='confirm_close'),
                  path('player/<int:player_id>/injuries/', views.player_injury_details, name='player_injury_details'),

                  path('add_treatment/<int:injury_id>/', views.add_treatment_recommendation, name='add_treatment'),
                 
               #    Oraganizatnion player management URLs
                  path('organization/player_add/', views.organization_player_add, name='organization_player_add'),
                  path('organization/player_list/', views.organization_player_list, name='organization_player_list'),
                  path('organization/player/<int:pk>/edit/', views.organization_player_edit, name='organization_player_edit'),
                  path('organization/player/<int:pk>/delete/', views.organization_player_delete, name='organization_player_delete'),
                  path('organization/player/<int:pk>/detail/', views.organization_player_detail, name='organization_player_detail'),
                  path('organization/player_export/', views.organization_player_export, name='organization_player_export'),

                  path('player/create/', views.player_create_view, name='player_create_view'),


               #   Organization injury management URLs
                  path('organization/injuries_list/', views.organization_injury_list, name='organization_injury_list'),  
                  path('organization/injuries/', views.organization_create_injury, name='organization_create_injury'),
                  path('ajax/get_player_info/<int:player_id>/', views.get_player_info, name='get_player_info'),
                  path('organization/injuries/<int:pk>/', views.organization_injury_detail, name='organization_injury_detail'),
                  path('organization/injuries/<int:pk>/edit/', views.organization_injury_edit, name='organization_injury_edit'),
                  path('organization/injuries/<int:pk>/delete/', views.organization_injury_delete, name='organization_injury_delete'),
                  path('organization/injuries/export/', views.organization_injury_export, name='organization_injury_export'),

                  path('organization/activity-logs/', views.activity_log_combined_view, name='activity_log_combined_view'),

               #   Organization camps and tournaments URLs
                  path('organization/camps_tournaments/', views.organization_camps_tournaments, name='organization_camps_tournaments'),
                  path('organization/camp/<int:camp_id>/', views.organization_camp_detail, name='organization_camp_detail'),
                  path('organization/camp/edit/<int:camp_id>/', views.organization_edit_camp, name='organization_edit_camp'),
                  path('organization/camp/create/', views.organization_create_camp, name='organization_create_camp'),
                  path('organization/camp/<int:camp_id>/delete/', views.organization_delete_camp, name='organization_delete_camp'),

                  path('organization/camp/<int:camp_id>/attendance/', views.camp_attendance_view, name='camp_attendance'),
                  path('ajax/filter-players-attendance/', views.filter_players_attendance, name='filter_players_attendance'),
                  path('organization/attendance-report/', views.attendance_report_view, name='attendance_report'),

                  path('organization/phase/<int:id>/', views.phase_tests_view, name='phase_tests_view'), 
                  path('organization/phase-test/<int:id>/',views.phase_test, name='phase_test'),
                  path('wellness-report/<int:camp_id>/', views.daily_wellness_camp_report, name='daily_wellness_camp_report'),
                  path('wellness/report/', views.wellness_dashboard, name='wellness_dashboard'),
                  # urls.py
                  path('player-wellness-report/', views.player_wellness_report, name='player_wellness_report'),


               # Organization Test Results URLs
                  # path('organization/test/dashboard', views.test_dashboard, name='test_dashboard'),
                  path('test/add/', views.add_test_result, name='add_test_result'),
                  path('organization/test-main/', views.test_results_main, name='test_results_main'),
                  path('organization/test-dashboard/', views.test_dashboard_new, name='test_dashboard_new'),
                  path('test-results/<str:test_name>/', views.test_results_view, name='test_results_by_name'),
                  path('add-test-results/<str:test_name>/', views.add_test_results, name='add_test_results'),

                  path('organization/dashboard/', views.organization_dashboard_org, name='organization_dashboard_org'),
                  path('org/players-by-category/', views.players_by_category, name='players_by_category'),           

                  path('teams-dashboard/', views.teams_dashboard, name='teams_dashboard'),

                  path('player-record/', views.player_record, name='player_record'),
                  path('player-data/', views.player_data, name='player_data'),
                  path('player-info/<int:player_id>/<str:test>/<str:start>/<str:end>/',views.player_info,name='player_info'),

                  path('get-players-by-test/', views.get_players_by_test, name='get_players_by_test'),
                  path('get-player-test-results/', views.get_player_test_results, name='get_player_test_results'),



                  path('new_test_details/',views.new_test_details, name='new_test_details'),  
                  path('nomative_data/',views.nomative_data, name='nomative_data'),
                  # path('new_test_dashboard/',views.new_test_dashboard, name='new_test_dashboard'),

                  path('report-settings/', views.report_settings_view, name='report_settings'),
                  path('save-report-settings/', views.save_report_settings_view, name='save_report_settings'),
                  path('delete-session/', views.delete_session, name='delete_session'),

                  # Test URLs
                  path('runa3x6/', views.add_run_3x6_test, name='add_run_3x6_test'),
                  path('glute-bridges/', views.add_glute_bridges_test, name='add_glute_bridges_test'),
                  path('lunge-calf-raises/', views.add_lunge_calf_raises_test, name='add_lunge_calf_raises_test'),
                  path('mb-rotational-throw/', views.add_mb_rotational_throw_test, name='add_mb_rotational_throw_test'),
                  path('copen-hagen/', views.add_copen_hagen_test, name='add_copen_hagen_test'),
                  path('sl-hop-test/', views.add_sl_hop_test, name='add_sl_hop_test'),
                  path('cmj-scores/', views.add_cmj_scores_test, name='add_cmj_scores_test'),
                  path('anthropometry/', views.add_anthropometry_test, name='add_anthropometry_test'),
                  path('dexa-scan/', views.add_dexa_scan_test, name='add_dexa_scan_test'),
                  path('blood-test/', views.add_blood_test, name='add_blood_tests_test'),
                  path('runa3/', views.add_runa3_test, name='add_runa3_test'),
                  path('forty-meter-test/', views.add_forty_meter_test, name='add_forty_meter_test'),
                  path('twenty-meter-test/', views.add_twenty_meter_test, name='add_twenty_meter_test'),
                  path('ten-meter-test/', views.add_ten_meter_test, name='add_ten_meter_test'),
                  path('sbj-test/', views.add_sbj_test, name='add_sbj_test'),
                  path('yoyo-test/', views.add_yoyo_test, name='add_yoyo_test'),
                  path('one-mile-test/', views.add_one_mile_test, name='add_one_mile_test'),
                  path('two-km-test/', views.add_two_km_test, name='add_two_km_test'),
                  path('pushups-test/', views.add_pushups_test, name='add_pushups_test'),
                  path('msk-injury-assessment/', views.add_msk_injury_assessment, name='add_msk_injury_assessment'),
                  path('organization/<int:player_id>/all-tests/', views.organization_player_tests,name='organization_player_tests'),
                  path('daily-wellness/',views.daily_wellness_create_view,name='daily_wellness_create_view'),


                  # Test Data View URLs
                  path('run-3x6-view/', views.run_3x6_test_view, name='run_3x6_test_view'),
                  path('glute-bridges-view/', views.glute_bridges_test_view, name='glute_bridges_test_view'),
                  path('lunge-calf-raises-view/', views.lunge_calf_raises_test_view, name='lunge_calf_raises_test_view'),
                  path('mb-rotational-throw-view/', views.mb_rotational_throw_test_view, name='mb_rotational_throw_test_view'),
                  path('copen-hagen-view/', views.copen_hagen_test_view, name='copen_hagen_test_view'),
                  path('sl-hop-view/', views.sl_hop_test_view, name='sl_hop_test_view'),
                  path('cmj-scores-view/', views.cmj_scores_test_view, name='cmj_scores_test_view'),
                  path('anthropometry-view/', views.anthropometry_test_view, name='anthropometry_test_view'),
                  path('dexa-scan-view/', views.dexa_scan_test_view, name='dexa_scan_test_view'),
                  path('blood-test-view/', views.blood_test_view, name='blood_test_view'),
                  path('runa3-view/',views.runa3_test_view, name='runa3_test_view'),
                  path('forty-meter-test-view/', views.forty_meter_test_view, name='forty_meter_test_view'),
                  path('twenty-meter-test-view/', views.twenty_meter_test_view, name='twenty_meter_test_view'),
                  path('ten-meter-test-view/', views.ten_meter_test_view, name='ten_meter_test_view'),
                  path('sbj-test-view/', views.sbj_test_view, name='sbj_test_view'),
                  path('yoyo-test-view/', views.yoyo_test_view, name='yoyo_test_view'),
                  path('one-mile-test-view/', views.one_mile_test_view, name='one_mile_test_view'),
                  path('two-km-test-view/', views.two_km_test_view, name='two_km_test_view'),
                  path('pushups-test-view/', views.pushups_test_view, name='pushups_test_view'),
                  path('msk-injury-assessment-list/', views.msk_injury_assessment_list, name='msk_injury_assessment_list'),
                  path('daily-wellness-view/',views.daily_wellness_results_view,name='daily_wellness_results_view'),
                  path('daily-wellness/filter-players/', views.filter_players_ajax, name='filter_players_ajax'),

                  # Daily Activity of Coachs
                  path('daily-log/<int:id>/',views.daily_activity_coach_log,name='daily_activity_coach_log'),
                  path('daily-snc-camp-detail/<int:pk>/',views.daily_snc_camp_detail, name='daily_snc_camp_detail'),
                  path('daily-log-list/<int:camp_id>/', views.daily_snc_camp_logs_list, name='daily_snc_camp_logs_list'),
                  path('snc-logs/', views.snc_camps_dashboard, name='snc_camps_dashboard'),

                  path('player-test-select/', views.player_test_select, name='player_test_select'),
                  path('fetch-players/', views.fetch_players, name='fetch_players'),
                  path('fetch-report/', views.fetch_report, name='fetch_report'),
                  path("player-report/", views.player_report, name="player_report"),
                  
                  # path('multi-test-report/', views.multi_test_report, name='multi_test_report'),
                  path('reports/multi-test/', views.multi_test_report_view, name='multi_test_report'),
                  path('ajax/fetch-multi-test-report/', views.fetch_multi_test_report, name='fetch_multi_test_report'),

                  path('multitest/',views.multitest,name='multitest'),

                  path('player-test-data/', views.get_player_test_data, name='player_test_data'),



              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
