-- Create model AcademicYear
--
CREATE TABLE `core_academicyear` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `year` integer UNSIGNED NOT NULL CHECK (`year` >= 0), `start_date` date NOT NULL, `end_date` date NOT NULL, `is_current` bool NOT NULL, `created_at` datetime(6) NOT NULL);
--
-- Create model Form
--
CREATE TABLE `core_form` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `level` integer UNSIGNED NOT NULL CHECK (`level` >= 0), `form_name` varchar(50) NOT NULL, `capacity` integer UNSIGNED NOT NULL CHECK (`capacity` >= 0));
--
-- Create model School
--
CREATE TABLE `core_school` (`id` char(32) NOT NULL PRIMARY KEY, `name` varchar(200) NOT NULL, `code` varchar(20) NOT NULL UNIQUE, `school_type` varchar(20) NOT NULL, `category` varchar(20) NOT NULL, `county` varchar(50) NOT NULL, `address` longtext NOT NULL, `phone` varchar(15) NOT NULL, `email` varchar(254) NOT NULL, `established_year` integer UNSIGNED NOT NULL CHECK (`established_year` >= 0), `capacity` integer UNSIGNED NOT NULL CHECK (`capacity` >= 0), `is_active` bool NOT NULL, `created_at` datetime(6) NOT NULL);
--
-- Create model Subject
--
CREATE TABLE `core_subject` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(100) NOT NULL, `code` varchar(10) NOT NULL UNIQUE, `subject_type` varchar(20) NOT NULL, `description` longtext NOT NULL);
--
-- Create model Fee
--
CREATE TABLE `core_fee` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(100) NOT NULL, `fee_type` varchar(20) NOT NULL, `amount` numeric(10, 2) NOT NULL, `is_compulsory` bool NOT NULL, `due_date` date NOT NULL, `academic_year_id` bigint NOT NULL, `form_id` bigint NULL, `school_id` char(32) NOT NULL);
--
-- Add field school to form
--
ALTER TABLE `core_form` ADD COLUMN `school_id` char(32) NOT NULL , ADD CONSTRAINT `core_form_school_id_2e66ba97_fk_core_school_id` FOREIGN KEY (`school_id`) REFERENCES `core_school`(`id`);
--
-- Add field school to academicyear
--
ALTER TABLE `core_academicyear` ADD COLUMN `school_id` char(32) NOT NULL , ADD CONSTRAINT `core_academicyear_school_id_31970e6c_fk_core_school_id` FOREIGN KEY (`school_id`) REFERENCES `core_school`(`id`);
--
-- Create model Term
--
CREATE TABLE `core_term` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `term_number` integer UNSIGNED NOT NULL CHECK (`term_number` >= 0), `start_date` date NOT NULL, `end_date` date NOT NULL, `is_current` bool NOT NULL, `academic_year_id` bigint NOT NULL);
--
-- Create model User
--
CREATE TABLE `core_user` (`password` varchar(128) NOT NULL, `last_login` datetime(6) NULL, `is_superuser` bool NOT NULL, `username` varchar(150) NOT NULL UNIQUE, `first_name` varchar(150) NOT NULL, `last_name` varchar(150) NOT NULL, `email` varchar(254) NOT NULL, `is_staff` bool NOT NULL, `is_active` bool NOT NULL, `date_joined` datetime(6) NOT NULL, `id` char(32) NOT NULL PRIMARY KEY, `user_type` varchar(20) NOT NULL, `phone_number` varchar(15) NOT NULL, `national_id` varchar(20) NULL UNIQUE, `date_of_birth` date NULL, `created_at` date NOT NULL, `updated_at` datetime(6) NOT NULL);
CREATE TABLE `core_user_groups` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `user_id` char(32) NOT NULL, `group_id` integer NOT NULL);  
CREATE TABLE `core_user_user_permissions` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `user_id` char(32) NOT NULL, `permission_id` integer NOT NULL);
--
-- Create model Teacher
--
CREATE TABLE `core_teacher` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `employee_number` varchar(20) NOT NULL UNIQUE, `tsc_number` varchar(20) NOT NULL, `qualifications` varchar(100) NOT NULL, `hire_date` date NOT NULL, `is_active` bool NOT NULL, `school_id` char(32) NOT NULL, `user_id` char(32) NOT NULL UNIQUE);
CREATE TABLE `core_teacher_subjects` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `teacher_id` bigint NOT NULL, `subject_id` bigint NOT NULL);
--
-- Create model Student
--
CREATE TABLE `core_student` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `admission_number` varchar(20) NOT NULL, `upi_number` varchar(20) NOT NULL UNIQUE, `gender` varchar(1) NOT NULL, `guardian_name` varchar(100) NOT NULL, `guardian_phone` varchar(15) NOT NULL, `guardian_email` varchar(254) NOT NULL, `admission_date` date NOT NULL, `kcpe_marks` integer UNSIGNED NOT NULL CHECK (`kcpe_marks` >= 0), `is_active` bool NOT NULL, `current_form_id` bigint NULL, `school_id` char(32) NOT NULL, `user_id` char(32) NOT NULL UNIQUE);
--
-- Add field principal to school
--
ALTER TABLE `core_school` ADD COLUMN `principal_id` char(32) NULL UNIQUE , ADD CONSTRAINT `core_school_principal_id_518f51eb_fk_core_user_id` FOREIGN KEY (`principal_id`) REFERENCES `core_user`(`id`);
--
-- Create model Parent
--
CREATE TABLE `core_parent` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `occupation` varchar(100) NOT NULL, `relationship_to_student` varchar(50) NOT NULL, `user_id` char(32) NOT NULL UNIQUE);
CREATE TABLE `core_parent_children` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `parent_id` bigint NOT NULL, `student_id` bigint NOT NULL);
--
-- Add field class_teacher to form
--
ALTER TABLE `core_form` ADD COLUMN `class_teacher_id` char(32) NULL , ADD CONSTRAINT `core_form_class_teacher_id_ee8008fc_fk_core_user_id` FOREIGN KEY (`class_teacher_id`) REFERENCES `core_user`(`id`);
--
-- Create model FeePayment
--
CREATE TABLE `core_feepayment` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `amount_paid` numeric(10, 2) NOT NULL, `payment_method` varchar(20) NOT NULL, `transaction_reference` varchar(50) NOT NULL, `payment_date` date NOT NULL, `receipt_number` varchar(50) NOT NULL UNIQUE, `created_at` datetime(6) NOT NULL, `fee_id` bigint NOT NULL, `student_id` bigint NOT NULL, `received_by_id` char(32) NOT NULL);
--
-- Create model Exam
--
CREATE TABLE `core_exam` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(100) NOT NULL, `exam_type` varchar(20) NOT NULL, `total_marks` integer UNSIGNED NOT NULL CHECK (`total_marks` >= 0), `exam_date` date NOT NULL, `created_at` datetime(6) NOT NULL, `academic_year_id` bigint NOT NULL, `form_id` bigint NOT NULL, `school_id` char(32) NOT NULL, `subject_id` bigint NOT NULL, `term_id` bigint NOT NULL, `created_by_id` char(32) NOT NULL);
--
-- Alter unique_together for academicyear (1 constraint(s))
--
ALTER TABLE `core_academicyear` ADD CONSTRAINT `core_academicyear_school_id_year_e4b0adfa_uniq` UNIQUE (`school_id`, `year`);
--
-- Create model StudentSubject
--
CREATE TABLE `core_studentsubject` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `enrolled_date` datetime(6) NOT NULL, `academic_year_id` bigint NOT NULL, `student_id` bigint NOT NULL, `subject_id` bigint NOT NULL, `teacher_id` bigint NULL);
--
-- Create model StudentExamResult
--
CREATE TABLE `core_studentexamresult` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `marks_obtained` integer UNSIGNED NOT NULL CHECK (`marks_obtained` >= 0), `grade` varchar(2) NOT NULL, `remarks` longtext NOT NULL, `entered_at` datetime(6) NOT NULL, `updated_at` datetime(6) NOT NULL, `exam_id` bigint NOT NULL, `student_id` bigint NOT NULL, `entered_by_id` char(32) NOT NULL);
--
-- Alter unique_together for form (1 constraint(s))
--
ALTER TABLE `core_form` ADD CONSTRAINT `core_form_school_id_form_name_0f4a61ff_uniq` UNIQUE (`school_id`, `form_name`);
--
-- Create model Attendance
--
CREATE TABLE `core_attendance` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `date` date NOT NULL, `status` varchar(20) NOT NULL, `remarks` longtext NOT NULL, `marked_at` datetime(6) NOT NULL, `student_id` bigint NOT NULL, `marked_by_id` char(32) NOT NULL);
ALTER TABLE `core_fee` ADD CONSTRAINT `core_fee_academic_year_id_6ca0f20d_fk_core_academicyear_id` FOREIGN KEY (`academic_year_id`) REFERENCES `core_academicyear` (`id`);
ALTER TABLE `core_fee` ADD CONSTRAINT `core_fee_form_id_5aba743d_fk_core_form_id` FOREIGN KEY (`form_id`) REFERENCES `core_form` (`id`);      
ALTER TABLE `core_fee` ADD CONSTRAINT `core_fee_school_id_d35f1b88_fk_core_school_id` FOREIGN KEY (`school_id`) REFERENCES `core_school` (`id`);
ALTER TABLE `core_term` ADD CONSTRAINT `core_term_academic_year_id_term_number_082e3ab8_uniq` UNIQUE (`academic_year_id`, `term_number`);     
ALTER TABLE `core_term` ADD CONSTRAINT `core_term_academic_year_id_77e94bd7_fk_core_academicyear_id` FOREIGN KEY (`academic_year_id`) REFERENCES `core_academicyear` (`id`);
ALTER TABLE `core_user_groups` ADD CONSTRAINT `core_user_groups_user_id_group_id_c82fcad1_uniq` UNIQUE (`user_id`, `group_id`);
ALTER TABLE `core_user_groups` ADD CONSTRAINT `core_user_groups_user_id_70b4d9b8_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);
ALTER TABLE `core_user_groups` ADD CONSTRAINT `core_user_groups_group_id_fe8c697f_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);
ALTER TABLE `core_user_user_permissions` ADD CONSTRAINT `core_user_user_permissions_user_id_permission_id_73ea0daa_uniq` UNIQUE (`user_id`, `permission_id`);
ALTER TABLE `core_user_user_permissions` ADD CONSTRAINT `core_user_user_permissions_user_id_085123d3_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);
ALTER TABLE `core_user_user_permissions` ADD CONSTRAINT `core_user_user_permi_permission_id_35ccf601_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);
ALTER TABLE `core_teacher` ADD CONSTRAINT `core_teacher_school_id_b7569a3f_fk_core_school_id` FOREIGN KEY (`school_id`) REFERENCES `core_school` (`id`);
ALTER TABLE `core_teacher` ADD CONSTRAINT `core_teacher_user_id_0d56ab99_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);
ALTER TABLE `core_teacher_subjects` ADD CONSTRAINT `core_teacher_subjects_teacher_id_subject_id_d0c3c778_uniq` UNIQUE (`teacher_id`, `subject_id`);
ALTER TABLE `core_teacher_subjects` ADD CONSTRAINT `core_teacher_subjects_teacher_id_c7d52cc5_fk_core_teacher_id` FOREIGN KEY (`teacher_id`) REFERENCES `core_teacher` (`id`);
ALTER TABLE `core_teacher_subjects` ADD CONSTRAINT `core_teacher_subjects_subject_id_20be280c_fk_core_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `core_subject` (`id`);
ALTER TABLE `core_student` ADD CONSTRAINT `core_student_school_id_admission_number_93b28b6c_uniq` UNIQUE (`school_id`, `admission_number`);   
ALTER TABLE `core_student` ADD CONSTRAINT `core_student_current_form_id_bd01f9da_fk_core_form_id` FOREIGN KEY (`current_form_id`) REFERENCES `core_form` (`id`);
ALTER TABLE `core_student` ADD CONSTRAINT `core_student_school_id_9d30b4f7_fk_core_school_id` FOREIGN KEY (`school_id`) REFERENCES `core_school` (`id`);
ALTER TABLE `core_student` ADD CONSTRAINT `core_student_user_id_666ccffd_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);
ALTER TABLE `core_parent` ADD CONSTRAINT `core_parent_user_id_f7fb215b_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);
ALTER TABLE `core_parent_children` ADD CONSTRAINT `core_parent_children_parent_id_student_id_775a5561_uniq` UNIQUE (`parent_id`, `student_id`);
ALTER TABLE `core_parent_children` ADD CONSTRAINT `core_parent_children_parent_id_4f56698d_fk_core_parent_id` FOREIGN KEY (`parent_id`) REFERENCES `core_parent` (`id`);
ALTER TABLE `core_parent_children` ADD CONSTRAINT `core_parent_children_student_id_22893756_fk_core_student_id` FOREIGN KEY (`student_id`) REFERENCES `core_student` (`id`);
ALTER TABLE `core_feepayment` ADD CONSTRAINT `core_feepayment_fee_id_48323609_fk_core_fee_id` FOREIGN KEY (`fee_id`) REFERENCES `core_fee` (`id`);
ALTER TABLE `core_feepayment` ADD CONSTRAINT `core_feepayment_student_id_654f44a8_fk_core_student_id` FOREIGN KEY (`student_id`) REFERENCES `core_student` (`id`);
ALTER TABLE `core_feepayment` ADD CONSTRAINT `core_feepayment_received_by_id_d7362061_fk_core_user_id` FOREIGN KEY (`received_by_id`) REFERENCES `core_user` (`id`);
ALTER TABLE `core_exam` ADD CONSTRAINT `core_exam_academic_year_id_af8c68d6_fk_core_academicyear_id` FOREIGN KEY (`academic_year_id`) REFERENCES `core_academicyear` (`id`);
ALTER TABLE `core_exam` ADD CONSTRAINT `core_exam_form_id_438f2e23_fk_core_form_id` FOREIGN KEY (`form_id`) REFERENCES `core_form` (`id`);    
ALTER TABLE `core_exam` ADD CONSTRAINT `core_exam_school_id_f2980dd8_fk_core_school_id` FOREIGN KEY (`school_id`) REFERENCES `core_school` (`id`);
ALTER TABLE `core_exam` ADD CONSTRAINT `core_exam_subject_id_82b2916c_fk_core_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `core_subject` (`id`);
ALTER TABLE `core_exam` ADD CONSTRAINT `core_exam_term_id_b11abd52_fk_core_term_id` FOREIGN KEY (`term_id`) REFERENCES `core_term` (`id`);    
ALTER TABLE `core_exam` ADD CONSTRAINT `core_exam_created_by_id_6974554d_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`);
ALTER TABLE `core_studentsubject` ADD CONSTRAINT `core_studentsubject_student_id_subject_id_ac_31cd24b4_uniq` UNIQUE (`student_id`, `subject_id`, `academic_year_id`);
ALTER TABLE `core_studentsubject` ADD CONSTRAINT `core_studentsubject_academic_year_id_16886b6c_fk_core_acad` FOREIGN KEY (`academic_year_id`) REFERENCES `core_academicyear` (`id`);
ALTER TABLE `core_studentsubject` ADD CONSTRAINT `core_studentsubject_student_id_e9856b7f_fk_core_student_id` FOREIGN KEY (`student_id`) REFERENCES `core_student` (`id`);
ALTER TABLE `core_studentsubject` ADD CONSTRAINT `core_studentsubject_subject_id_3aee5236_fk_core_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `core_subject` (`id`);
ALTER TABLE `core_studentsubject` ADD CONSTRAINT `core_studentsubject_teacher_id_c21eb2c5_fk_core_teacher_id` FOREIGN KEY (`teacher_id`) REFERENCES `core_teacher` (`id`);
ALTER TABLE `core_studentexamresult` ADD CONSTRAINT `core_studentexamresult_exam_id_student_id_d6137d80_uniq` UNIQUE (`exam_id`, `student_id`);
ALTER TABLE `core_studentexamresult` ADD CONSTRAINT `core_studentexamresult_exam_id_dba280ed_fk_core_exam_id` FOREIGN KEY (`exam_id`) REFERENCES `core_exam` (`id`);
ALTER TABLE `core_studentexamresult` ADD CONSTRAINT `core_studentexamresult_student_id_0d080079_fk_core_student_id` FOREIGN KEY (`student_id`) REFERENCES `core_student` (`id`);
ALTER TABLE `core_studentexamresult` ADD CONSTRAINT `core_studentexamresult_entered_by_id_ff1dae0a_fk_core_user_id` FOREIGN KEY (`entered_by_id`) REFERENCES `core_user` (`id`);
ALTER TABLE `core_attendance` ADD CONSTRAINT `core_attendance_student_id_date_900e3f9a_uniq` UNIQUE (`student_id`, `date`);
ALTER TABLE `core_attendance` ADD CONSTRAINT `core_attendance_student_id_681381f8_fk_core_student_id` FOREIGN KEY (`student_id`) REFERENCES `core_student` (`id`);
ALTER TABLE `core_attendance` ADD CONSTRAINT `core_attendance_marked_by_id_70c30462_fk_core_user_id` FOREIGN KEY (`marked_by_id`) REFERENCES `core_user` (`id`);