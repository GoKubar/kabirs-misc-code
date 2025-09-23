public class PDController {
    private double kP;
    private double kD;
    private double previousError = 0;
    
    public PDController(double kP, double kD) {
        this.kP = kP;
        this.kD = kD;
    }
    
    public double calculate(double target, double current) {
        double error = target - current;
        double derivative = error - previousError;
        previousError = error;
        
        return (kP * error) + (kD * derivative);
    }
}