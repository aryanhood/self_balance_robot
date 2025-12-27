def complementary_filter_step(acc_angle, gyro_rate, dt, alpha, prev_angle):
    # acc_angle: angle estimate from accelerometer (deg)
    # gyro_rate: angular rate from gyro (deg/s)
    # dt: timestep in seconds
    # alpha: complementary filter mixing parameter
    # prev_angle: previous angle estimate (deg)
    # returns new angle estimate
    gyro_angle = prev_angle + gyro_rate * dt
    fused = alpha * gyro_angle + (1 - alpha) * acc_angle
    return fused
