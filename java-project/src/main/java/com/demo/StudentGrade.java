package com.demo;

public class StudentGrade {

    public String calculateGrade(int marks, boolean attendanceOk) {

        if (attendanceOk == false) {
            return "FAIL_ATTENDANCE";
        }

        if (marks < 0 || marks > 100) {
            return "INVALID_MARKS";
        }

        if (marks >= 90) {
            return "A+";
        }
        else if (marks >= 80) {
            return "A";
        }
        else if (marks >= 70) {
            return "B";
        }
        else if (marks >= 60) {
            return "C";
        }
        else if (marks >= 40) {

            if (marks >= 50) {
                return "D";
            } else {
                return "E";
            }

        }
        else {
            return "FAIL";
        }
    }
}

