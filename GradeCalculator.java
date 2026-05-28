import java.util.*;

public class GradeCalculator {
    private HashMap<String, ArrayList<Integer>> students;
    private Scanner scanner;

    public GradeCalculator() {
        this.students = new HashMap<>();
        this.scanner = new Scanner(System.in);
    }

    // Add a new student
    public void addStudent(String name) {
        if (name == null || name.trim().isEmpty()) {
            System.out.println("Error: Student name cannot be empty!");
            return;
        }

        if (students.containsKey(name)) {
            System.out.println("Error: Student '" + name + "' already exists!");
            return;
        }

        students.put(name, new ArrayList<>());
        System.out.println("Student '" + name + "' added successfully!");
    }

    // Add a grade to a student
    public void addGrade(String name, int grade) {
        if (!students.containsKey(name)) {
            System.out.println("Error: Student '" + name + "' not found!");
            return;
        }

        if (grade < 0 || grade > 100) {
            System.out.println("Error: Grade must be between 0 and 100!");
            return;
        }

        students.get(name).add(grade);
        System.out.println("Grade " + grade + " added for '" + name + "'!");
    }

    // Calculate average for a specific student
    public void calculateStudentAverage(String name) {
        if (!students.containsKey(name)) {
            System.out.println("Error: Student '" + name + "' not found!");
            return;
        }

        ArrayList<Integer> grades = students.get(name);

        if (grades.isEmpty()) {
            System.out.println("Error: Student '" + name + "' has no grades yet!");
            return;
        }

        double average = 0;
        for (int grade : grades) {
            average += grade;
        }
        average /= grades.size();

        System.out.println("\nStudent: " + name);
        System.out.println("Grades: " + grades);
        System.out.println("Average: " + String.format("%.2f", average));
        System.out.println();
    }

    // Calculate class average
    public void calculateClassAverage() {
        if (students.isEmpty()) {
            System.out.println("Error: No students in the system!");
            return;
        }

        double totalGrades = 0;
        int gradeCount = 0;

        for (ArrayList<Integer> grades : students.values()) {
            if (grades.isEmpty()) {
                continue;
            }
            for (int grade : grades) {
                totalGrades += grade;
                gradeCount++;
            }
        }

        if (gradeCount == 0) {
            System.out.println("Error: No grades have been entered yet!");
            return;
        }

        double classAverage = totalGrades / gradeCount;
        System.out.println("\n=== Class Statistics ===");
        System.out.println("Total Students: " + students.size());
        System.out.println("Total Grades: " + gradeCount);
        System.out.println("Class Average: " + String.format("%.2f", classAverage));
        System.out.println();
    }

    // Display menu and get user choice
    public int displayMenu() {
        System.out.println("\n========== Grade Calculator Menu ==========");
        System.out.println("1. Add a Student");
        System.out.println("2. Add a Grade to Student");
        System.out.println("3. Calculate Student Average");
        System.out.println("4. Calculate Class Average");
        System.out.println("5. Exit");
        System.out.println("==========================================");
        System.out.print("Enter your choice (1-5): ");

        int choice = -1;
        try {
            choice = scanner.nextInt();
            scanner.nextLine(); // Consume newline
            if (choice < 1 || choice > 5) {
                System.out.println("Error: Please enter a number between 1 and 5!");
                return -1;
            }
        } catch (InputMismatchException e) {
            System.out.println("Error: Invalid input! Please enter a number.");
            scanner.nextLine(); // Consume invalid input
            return -1;
        }
        return choice;
    }

    // Run the grade calculator application
    public void run() {
        System.out.println("\n===== Welcome to Grade Calculator =====");

        boolean running = true;
        while (running) {
            int choice = displayMenu();

            if (choice == -1) {
                continue;
            }

            switch (choice) {
                case 1:
                    // Add a Student
                    System.out.print("Enter student name: ");
                    String name = scanner.nextLine().trim();
                    addStudent(name);
                    break;

                case 2:
                    // Add a Grade
                    System.out.print("Enter student name: ");
                    name = scanner.nextLine().trim();

                    if (!students.containsKey(name)) {
                        System.out.println("Error: Student '" + name + "' not found!");
                        break;
                    }

                    System.out.print("Enter grade (0-100): ");
                    try {
                        int grade = scanner.nextInt();
                        scanner.nextLine(); // Consume newline
                        addGrade(name, grade);
                    } catch (InputMismatchException e) {
                        System.out.println("Error: Invalid input! Please enter a number.");
                        scanner.nextLine(); // Consume invalid input
                    }
                    break;

                case 3:
                    // Calculate Student Average
                    System.out.print("Enter student name: ");
                    name = scanner.nextLine().trim();
                    calculateStudentAverage(name);
                    break;

                case 4:
                    // Calculate Class Average
                    calculateClassAverage();
                    break;

                case 5:
                    // Exit
                    System.out.println("\nThank you for using Grade Calculator. Goodbye!");
                    running = false;
                    break;

                default:
                    System.out.println("Error: Invalid choice!");
            }
        }
    }

    public static void main(String[] args) {
        GradeCalculator calculator = new GradeCalculator();
        calculator.run();
    }
}
