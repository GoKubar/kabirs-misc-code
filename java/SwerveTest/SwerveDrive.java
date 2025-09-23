public class SwerveDrive {
    private SwervePod[] pods;

    public SwerveDrive(double[] pod1Offsets, double[] pod2Offsets, double[] pod3Offsets, double[] pod4Offsets) {
        pods = new SwervePod[4];
        double kP = 0.1;
        double kD = 0.0;
        
        pods[0] = new SwervePod(kP, kD, 0, pod1Offsets[0], pod1Offsets[1]);
        pods[1] = new SwervePod(kP, kD, 0, pod2Offsets[0], pod2Offsets[1]);
        pods[2] = new SwervePod(kP, kD, 0, pod3Offsets[0], pod3Offsets[1]);
        pods[3] = new SwervePod(kP, kD, 0, pod4Offsets[0], pod4Offsets[1]);
    }

    public void updateRaw(double leftStickX, double leftStickY, double rightStickX, double headingDegrees, double speed, double rotSpeed) {
        double y = leftStickY;
        double x = leftStickX;
        double rx = (Math.abs(rightStickX) < 0.05) ? 0 : rightStickX * rotSpeed;
        
        double headingRadians = Math.toRadians(headingDegrees);

        Vector[] podVectors = new Vector[pods.length];

        System.out.println(String.format("Input - X: %.2f, Y: %.2f, RX: %.2f, Heading: %.1f°", x, y, rx, headingDegrees));

        for (int podNum = 0; podNum < pods.length; podNum++) {
            SwervePod pod = pods[podNum];
            Vector rawTrans = new Vector(x, y);
            Vector translation = rawTrans.getMagnitude() < 0.05 ? new Vector(0, 0)
                    : rawTrans.rotate(-headingRadians).multiply(speed);
            Vector rotation = (new Vector(pod.getXOffset(), pod.getYOffset()));
            rotation = rotation.rotate(Math.PI / 2);
            rotation = rotation.divide(rotation.getMagnitude() == 0 ? 1 : rotation.getMagnitude());
            rotation = rotation.multiply(-rx);
            podVectors[podNum] = translation.add(rotation);
            
            System.out.println(String.format("Pod %d - Translation: (%.2f, %.2f), Rotation: (%.2f, %.2f)", 
                podNum, translation.getMagnitude() * Math.cos(translation.getArgument()), 
                translation.getMagnitude() * Math.sin(translation.getArgument()),
                rotation.getMagnitude() * Math.cos(rotation.getArgument()),
                rotation.getMagnitude() * Math.sin(rotation.getArgument())));
        }
        
        double maxMagnitude = 1;
        for (int i = 0; i < podVectors.length; i++) {
            maxMagnitude = Math.max(maxMagnitude, podVectors[i].getMagnitude());
        }
        if (maxMagnitude > 1) {
            maxMagnitude = 1;
        }
        
        System.out.println(String.format("Max magnitude before normalization: %.2f", maxMagnitude));
        
        for (int podNum = 0; podNum < pods.length; podNum++) {
            Vector finalVector = podVectors[podNum].divide(maxMagnitude);
            System.out.println(String.format("Pod %d final vector - Mag: %.2f, Angle: %.2f°", 
                podNum, finalVector.getMagnitude(), Math.toDegrees(finalVector.getArgument())));
            pods[podNum].move(finalVector.getArgument(), finalVector.getMagnitude());
        }
        System.out.println("---");
    }

    public String getDriveModeName() {
        return "Swerve Drive";
    }
}