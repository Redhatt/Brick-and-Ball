import numpy as np
import math, scipy, time


class Quaternions:
    def __init__(self, *args, unit=True):
        if unit:
            # quat --> [w,x,y,z]
            if len(args) == 1:
                self.w = args[0][0]
                self.x = args[0][1]  # defining all four dimensions...
                self.y = args[0][2]
                self.z = args[0][3]
                self.quat = np.array([self.w, self.x, self.y, self.z])  # defining quat...
                self.norm = np.linalg.norm(self.quat)
                if self.norm != 1:
                    self.quat = np.array([self.w, self.x, self.y, self.z]) / self.norm  # converting into unit quat...
                self.angle = math.acos(self.w / self.norm)
                self.angle_deg = math.degrees(math.acos(self.w / self.norm))
                self.vec_norm = np.linalg.norm(np.array([self.x, self.y, self.z]))
                #self.quat_ang = f"(cos({self.angle * (180 / np.pi)}), sin({self.angle * (180 / np.pi)})({self.x / self.vec_norm}i, {self.x / self.vec_norm}j, {self.x / self.vec_norm}k))"
                self.quat_form = f"{self.w}, ({self.x}i, {self.y}j, {self.z}k)"  # to print quat into its format...

            # quat --> [angle, (i, j, k)]
            elif len(args) == 2:
                self.angle = args[0]
                self.vec = np.array(args[1])
                self.vec_norm = np.linalg.norm(self.vec)
                if self.vec_norm<1e-14:
                    self.vector = np.array([0,0,0])
                elif self.vec_norm != 1:
                    self.vec = self.vec / self.vec_norm  # converting into unit quat...
                self.quat = np.array(
                    [math.cos(self.angle), 
                     self.vec[0] * math.sin(self.angle),
                     self.vec[1] * math.sin(self.angle), 
                     self.vec[2] * math.sin(self.angle)])
                self.quat_form = f"({self.quat[0]}, ({self.quat[1]}i, {self.quat[2]}j, {self.quat[3]}k))"
                #self.quat_ang = f"(cos({self.angle * (180 / np.pi)}), sin({self.angle * (180 / np.pi)})({self.vec[0]}i, {self.vec[1]}j, {self.vec[2]}k))"
        else:
            if len(args) == 1:
                self.w = args[0][0]
                self.x = args[0][1]  # defining all four dimensions...
                self.y = args[0][2]
                self.z = args[0][3]
                self.quat = np.array([self.w, self.x, self.y, self.z])  # defining quat...
                self.norm = np.linalg.norm(self.quat)
                if self.norm<1e-15:
                    self.quat = np.array([0,0,0,0])
                    self.angle = math.acos(0)
                    self.angle_deg = math.degrees(math.acos(0))
                    self.vec_norm = 0
                else:
                    self.angle = math.acos(self.w / self.norm)
                    self.angle_deg = math.degrees(math.acos(self.w / self.norm))
                    self.vec_norm = np.linalg.norm(np.array([self.x, self.y, self.z]))
                #self.quat_ang = f"{self.norm}[(cos({self.angle * (180 / np.pi)}), sin({self.angle * (180 / np.pi)})({self.x / self.vec_norm}i, {self.x / self.vec_norm}j, {self.x / self.vec_norm}k)]"
                self.quat_form = f"{self.w}, ({self.x}i, {self.y}j, {self.z}k)"  # to print quat into its format...

    def inverse(self):
        quat = -self.quat
        quat[0] = -quat[0]
        return Quaternions(quat, unit=False)

    def details(self):
        print("____________________________Details_________________________________________________________________________")
        print(f"quaternion:                {self.quat}")
        print(f"actual quaternion:         {self.quat_form}")
        print(f"angle of quaternion:       {self.angle} radians\n"
              f"                           {self.angle_deg} degrees")
        print(f"norm of quaternion:        {self.norm}")
        print(f"vector norm of quaternion: {self.vec_norm}")
        print("____________________________________________________________________________________________________________")
        print("")

def qadd(*args):
    if any(arg.__class__.__name__ != "Quaternions" for arg in args):
        raise TypeError("Not form Quaternions class")
    summ = np.array([0, 0, 0, 0], dtype='float64')
    for quat in args:
        summ += quat.quat
    return Quaternions(summ, unit=False)


def qmul(quat1, quat2):
    if quat1.__class__.__name__ != "Quaternions" and quat2.__class__.__name__ != "Quaternions":
        raise TypeError("Not form Quaternions class")
    w1 = quat1.quat[0]
    w2 = quat2.quat[0]
    v1 = quat1.quat[1:4]
    v2 = quat2.quat[1:4]
    w = w1 * w2 - (np.dot(v1, v2))
    v = w1 * v2 + w2 * v1 + np.cross(v1, v2)
    return Quaternions(np.concatenate([np.array([w]), v]), unit=False)


def qrot_quat(rotation, vector, point=np.array([0,0,0])):
    '''answer = rotation X vector X rotation_inverse'''
    if rotation.__class__.__name__ != "Quaternions" or vector.__class__.__name__ != "Quaternions":
        raise TypeError("Not form Quaternions class")
    if np.linalg.norm(rotation.quat) != 1:
        raise TypeError("rotation quat not unit quat.")
    if vector.quat[0] != 0:
        raise TypeError("vector[0] not equal to zero.")

    w = rotation.quat[0]
    v = rotation.quat[1:4]
    v_prime = vector.quat[1:4]-point
    q_final = v_prime*(np.square(w) - np.dot(v, v)) + 2 * (np.dot(v, v_prime)) * v + 2 * w * (np.cross(v, v_prime))
    return np.array(q_final)+point

def qrot_vec(vector, angle, axis, point=np.array([0,0,0])):
    '''answer = angle X vector X angle_inverse'''
    rotation = Quaternions(angle/2, axis)
    vector = vec2quat(np.array(vector) - point)
    w = rotation.quat[0]
    v = rotation.quat[1:4]
    v_prime = vector.quat[1:4]
    q_final = v_prime*(np.square(w) - np.dot(v, v)) + 2 * (np.dot(v, v_prime)) * v + 2 * w * (np.cross(v, v_prime))
    result = np.array(q_final) + point
    return result

def quat2vec(quat):
    if quat.__class__.__name__ != "Quaternions":
       raise TypeError("Not form Quaternions class")
    if quat.quat[0] != 0:
        raise TypeError("vector[0] not equal to zero.")
    return quat.qaut[1:4]


def vec2quat(vec, value=False):
    vec = np.concatenate([[0], vec])
    return Quaternions(vec, unit=value)

# examples: how to use this script...
if __name__ == '__main__':
    q1 = Quaternions([1,2,3,4])
    q1.details()

    q2 = Quaternions([1,1,1,1])
    q2.details()

    q_add = qadd(q1, q2)
    q_add.details()

    rotation = math.pi/2
    axis = np.array([0,0,1])
    vector = [1,0,0]

    #rot_vec_1 = qrot_quat(Quaternions(rotation/2, axis), vec2quat(vector), point=np.array([1,1,1]))
    rot_vec_2 = qrot_vec(vector, rotation, axis)
    #print(rot_vec_1)
    print(rot_vec_2)

