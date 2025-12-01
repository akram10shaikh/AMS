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

               # Organization Test Results URLs
                  # path('organization/test/dashboard', views.test_dashboard, name='test_dashboard'),
                  path('test/add/', views.add_test_result, name='add_test_result'),
                  path('organization/test-main/', views.test_results_main, name='test_results_main'),
                  path('organization/test-dashboard/', views.test_dashboard_new, name='test_dashboard_new'),
                  path('test-results/<str:test_name>/', views.test_results_view, name='test_results_by_name'),
                  path('add-test-results/<str:test_name>/', views.add_test_results, name='add_test_results'),

                  path('organization/dashboard/', views.organization_dashboard_org, name='organization_dashboard_org'),
                 

                  path('teams-dashboard/', views.teams_dashboard, name='teams_dashboard'),

                  path('player-record/', views.player_record, name='player_record'),
                  path('player-data/', views.player_data, name='player_data'),
                  path('player-info/<int:player_id>/<str:test>/<str:start>/<str:end>/', views.player_info, name='player_info'),
                  path('get-players-by-test/', views.get_players_by_test, name='get_players_by_test'),
                  path('get-player-test-results/', views.get_player_test_results, name='get_player_test_results'),



                  path('new_test_details/',views.new_test_details, name='new_test_details'),  
                  path('nomative_data/',views.nomative_data, name='nomative_data'),
                  # path('new_test_dashboard/',views.new_test_dashboard, name='new_test_dashboard'),

                  path('report-settings/', views.report_settings_view, name='report_settings'),
                  path('save-report-settings/', views.save_report_settings_view, name='save_report_settings'),
                  path('delete-session/', views.delete_session, name='delete_session'),

                  # Test URLs
                  path('runa3x6/<str:test_name>/', views.add_run_3x6_test, name='add_run_3x6_test'),
                  path('glute-bridges/<str:test_name>/', views.add_glute_bridges_test, name='add_glute_bridges_test'),
                  path('lunge-calf-raises/<str:test_name>/', views.add_lunge_calf_raises_test, name='add_lunge_calf_raises_test'),
                  path('mb-rotational-throw/<str:test_name>/', views.add_mb_rotational_throw_test, name='add_mb_rotational_throw_test'),
                  path('copen-hagen/<str:test_name>/', views.add_copen_hagen_test, name='add_copen_hagen_test'),
                  path('sl-hop/<str:test_name>/', views.add_sl_hop_test, name='add_sl_hop_test'),
                  path('cmj-scores/<str:test_name>/', views.add_cmj_scores_test, name='add_cmj_scores_test'),
                  path('anthropometry/<str:test_name>/', views.add_anthropometry_test, name='add_anthropometry_test'),
                  path('dexa-scan/<str:test_name>/', views.add_dexa_scan_test, name='add_dexa_scan_test'),
                  path('blood-test/<str:test_name>/', views.add_blood_test, name='add_blood_tests_test'),
                  path('runa3/<str:test_name>/', views.add_runa3_test, name='add_runa3_test'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
