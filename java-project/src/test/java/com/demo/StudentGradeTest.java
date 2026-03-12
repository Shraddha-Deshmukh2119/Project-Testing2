package com.demo;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

public class StudentGradeTest {

    StudentGrade grade = new StudentGrade();

    @Test
    void testTopper() {
        assertEquals("A+", grade.calculateGrade(95, true));
    }

    @Test
    void testAverageStudent() {
        assertEquals("B", grade.calculateGrade(72, true));
    }

    @Test
    void testLowPass() {
        assertEquals("E", grade.calculateGrade(45, true));
    }
    @Test
void testInvalidMarks() {
    assertEquals("INVALID_MARKS", grade.calculateGrade(-10, true));
}

@Test
void testFail() {
    assertEquals("FAIL", grade.calculateGrade(20, true));
}


    @Test
    void testFailDueToAttendance() {
        assertEquals("FAIL_ATTENDANCE", grade.calculateGrade(80, false));
    }
}
