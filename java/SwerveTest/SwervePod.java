public class SwervePod {
    private final PDController anglePID;
    private final double angleOffset;
    private final double xOffset;
    private final double yOffset;
    private boolean powerReversed = false;
    private double currentAngle = 0;

    public SwervePod(double kP, double kD, double angleOffset, double xOffset, double yOffset) {
        this.anglePID = new PDController(kP, kD);
        this.angleOffset = angleOffset;
        this.xOffset = xOffset;
        this.yOffset = yOffset;
    }

    public void move(double targetAngle, double power) {
        double actualDeg = normalize0To360(currentAngle + angleOffset);
        double desiredDeg = normalize0To360(Math.toDegrees(targetAngle));

        double error = shortestAngleToTarget(actualDeg, desiredDeg);

        if (Math.abs(error) > 90.0) {
            desiredDeg = normalize0To360(desiredDeg + 180.0);
            power = -power;
            error = shortestAngleToTarget(actualDeg, desiredDeg);
        }

        double setpointDeg = actualDeg + error;
        double pidf = anglePID.calculate(setpointDeg, actualDeg);
        double servoPower = Math.max(-1.0, Math.min(pidf, 1.0));
        
        currentAngle += servoPower * 0.1;

        System.out.println(String.format("Pod - Target Angle: %.2f°, Current: %.2f°, Servo: %.2f, Motor: %.2f", 
            desiredDeg, actualDeg, servoPower, power));
    }

    public double getYOffset() {
        return yOffset;
    }

    public double getXOffset() {
        return xOffset;
    }

    private static double normalize0To360(double deg) {
        deg = deg % 360.0;
        if (deg < 0)
            deg += 360.0;
        return deg;
    }

    private static double shortestAngleToTarget(double current, double target) {
        current = normalize0To360(current);
        target = normalize0To360(target);

        double delta = target - current;
        if (delta > 180)
            delta -= 360;
        else if (delta <= -180)
            delta += 360;

        if (Math.abs(delta) == 180)
            return -180;
        return delta;
    }
}