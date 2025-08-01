import { Injectable, NotFoundException } from "@nestjs/common";
import { InjectRepository } from "@nestjs/typeorm";
import { FindOneOptions, Repository } from "typeorm";
import { User } from "./user.entity";
import { CreateUserDto } from "./dto/create-user.dto";
import { UpdateUserDto } from "./dto/update-user.dto";

@Injectable()
export class UserService{
    constructor(
        @InjectRepository(User)
        private readonly userRepository: Repository<User>,
    ) {}

    async create(createUserDto: CreateUserDto): Promise<User> {
        const user = this.userRepository.create(createUserDto);
        return await this.userRepository.save(user);
    }

    async findAll(): Promise<User[]> {
        return await this.userRepository.find();
    }

    async findOne(id: number): Promise<User>{
        const options: FindOneOptions<User> = {where: {id}};
        const user = await this.userRepository.findOne(options);

        if(!user){
            throw new NotFoundException(`User with id ${id} not found`);
        }
        return user;
    }

    async findByTelegramId(telegramId: string): Promise<User | null> {
        return await this.userRepository.findOne({ where: { telegramId } });
    }

    async update(id: number, updateUserDto: UpdateUserDto): Promise<User>{
        const user = await this.findOne(id);
        this.userRepository.merge(user, updateUserDto);
        return await this.userRepository.save(user);
    }

    async remove(id: number): Promise<void>{
        const user = await this.findOne(id);
        await this.userRepository.remove(user);
    }

    async deactivate(id: number): Promise<User>{
        const user = await this.findOne(id);
        user.isActive = false;
        return await this.userRepository.save(user);
    }
    
    async userExists(telegramId: string): Promise<boolean> {
        const count = await this.userRepository.count({ where: { telegramId } });
        return count > 0;
    }
}