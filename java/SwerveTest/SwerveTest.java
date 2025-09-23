import java.util.Scanner;

public class SwerveTest {
  public static void main(String[] args) {
    SwerveDrive swerveDrive = new SwerveDrive(new double[] { 5, 5 }, // Pod 1 offsets
        new double[] { -5, 5 }, // Pod 2 offsets
        new double[] { 5, -5 }, // Pod 3 offsets
        new double[] { -5, -5 } // Pod 4 offsets
    );

    Scanner scanner = new Scanner(System.in);

    System.out.println("Swerve Drive Simulation");
    System.out.println("Enter 'quit' to exit");
    System.out.println("Heading: 0° = forward, positive = clockwise, range [-180, 180)");
    System.out.println();

    while (true) {
      try {
        System.out.print("Enter leftStickX: ");
        if (!scanner.hasNext())
          break;
        String input = scanner.next();
        if (input.equalsIgnoreCase("quit"))
          break;
        double leftStickX = Double.parseDouble(input);

        System.out.print("Enter leftStickY: ");
        if (!scanner.hasNext())
          break;
        input = scanner.next();
        if (input.equalsIgnoreCase("quit"))
          break;
        double leftStickY = Double.parseDouble(input);

        System.out.print("Enter rightStickX: ");
        if (!scanner.hasNext())
          break;
        input = scanner.next();
        if (input.equalsIgnoreCase("quit"))
          break;
        double rightStickX = Double.parseDouble(input);

        System.out.print("Enter heading (degrees): ");
        if (!scanner.hasNext())
          break;
        input = scanner.next();
        if (input.equalsIgnoreCase("quit"))
          break;
        double heading = Double.parseDouble(input);

        System.out.println();
        swerveDrive.updateRaw(leftStickX, leftStickY, rightStickX, heading, 1.0, 1.0);
        System.out.println();

      } catch (NumberFormatException e) {
        System.out.println("Invalid input. Please enter numbers or 'quit'.");
      } catch (Exception e) {
        System.out.println("Error: " + e.getMessage());
        break;
      }
    }

    scanner.close();
    System.out.println("Swerve simulation ended.");
  }
}
